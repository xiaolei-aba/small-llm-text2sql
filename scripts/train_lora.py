"""Single GPU LoRA with fixed exposure budget, train-only sampling and exact resume."""
import argparse
import hashlib
import json
import math
import random
import subprocess
import sys
import time
import traceback
from datetime import datetime,timezone
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--config',required=True)
    ap.add_argument('--resume-note',default='automatic recovery')
    args=ap.parse_args()
    if Path(sys.prefix).name!='text2sql': raise RuntimeError('Use text2sql')
    import torch
    import torch.nn.functional as F
    from src.utils.model_loading import load_base,compute_context
    from peft import LoraConfig,get_peft_model,get_peft_model_state_dict,set_peft_model_state_dict
    config=json.loads((ROOT/args.config).read_text())
    lock=json.loads((ROOT/'configs/model_lock.json').read_text())
    manifest=json.loads((ROOT/'data/manifests/sft_train.json').read_text())
    source=ROOT/'data/processed/sft_train.jsonl'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['processed_sha256']
    rows=[json.loads(l) for l in source.read_text().splitlines()]
    assert len(rows)==7000 and max(len(r['input_ids']) for r in rows)<=config['max_sequence_length']
    run=config['run_id']; dest=ROOT/'adapters'/run
    report=ROOT/'results'/f'{run}_training.json'
    previous_report=json.loads(report.read_text()) if report.exists() else {}
    checkpoint=ROOT/'checkpoints'/run/'latest.pt'
    if (dest/'adapter_model.safetensors').exists():
        if report.exists() and json.loads(report.read_text()).get('status')=='completed':
            print('Completed adapter preserved; no training repeated');return
        raise RuntimeError('Existing final adapter without completed report; inspect before overwrite')
    if not (ROOT/'results/e0_dev_summary.json').exists():
        raise RuntimeError('Finish full E0 before training')
    config_hash=hashlib.sha256(json.dumps([config,lock,manifest['processed_sha256']],sort_keys=True).encode()).hexdigest()
    rng=random.Random(config['seed'])
    if config['sampling_policy']=='uniform_without_replacement':
        order=list(range(len(rows)));rng.shuffle(order)
        assert config['examples_budget']<=len(order)
        order=order[:config['examples_budget']]
    else:
        weights=[config['difficulty_weights'][r['difficulty']] for r in rows]
        order=rng.choices(range(len(rows)),weights=weights,k=config['examples_budget'])
    from src.train.weighting import normalized_loss_weights
    loss_weights=normalized_loss_weights(rows,order,config.get('loss_difficulty_weights'))
    if config.get('control_order_manifest'):
        control=json.loads((ROOT/config['control_order_manifest']).read_text())
        assert order==control['indices'], 'E3 must keep the exact E1 sample order'
    order_path=ROOT/'data/manifests'/f'{run}_order.json'
    order_record={'config_hash':config_hash,'indices':order,'counts':dict(Counter(rows[i]['difficulty'] for i in order)),
                  'unique_samples':len(set(order)),'examples':len(order),
                  'sequence_tokens':sum(len(rows[i]['input_ids']) for i in order),
                  'target_tokens':sum(rows[i]['target_tokens'] for i in order)}
    if config.get('loss_difficulty_weights'):
        order_record['loss_weights_by_difficulty']={r['difficulty']:w for r,w in zip(rows,loss_weights)}
        order_record['mean_exposure_loss_weight']=sum(loss_weights[i] for i in order)/len(order)
    order_path.write_text(json.dumps(order_record,indent=2)+'\n')
    torch.manual_seed(config['seed']);torch.cuda.manual_seed_all(config['seed'])
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported(): raise RuntimeError('BF16 CUDA required')
    quantization=config.get('quantization','none')
    model=load_base(ROOT/lock['local_dir'],quantization)
    model.config.use_cache=False
    model=get_peft_model(model,LoraConfig(r=config['rank'],lora_alpha=config['alpha'],lora_dropout=config['dropout'],
                          target_modules=config['target_modules'],bias='none',task_type='CAUSAL_LM'))
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    model.enable_input_require_grads();model.train()
    params=[p for p in model.parameters() if p.requires_grad]
    assert all('lora_' in name for name,p in model.named_parameters() if p.requires_grad)
    optimizer=torch.optim.AdamW(params,lr=config['learning_rate'],weight_decay=config['weight_decay'])
    accum=config['gradient_accumulation_steps'];steps=math.ceil(len(order)/accum)
    history=[];start_step=0;prior_time=0.;prior_peak=0;prior_reserved=0
    if checkpoint.exists():
        state=torch.load(checkpoint,map_location='cpu',weights_only=False)
        assert state['config_hash']==config_hash
        set_peft_model_state_dict(model,state['adapter']);optimizer.load_state_dict(state['optimizer'])
        torch.set_rng_state(state['cpu_rng']);torch.cuda.set_rng_state_all(state['cuda_rng'])
        start_step=state['step'];history=state['history'];prior_time=state['train_seconds']
        prior_peak=state['peak_allocated_bytes'];prior_reserved=state['peak_reserved_bytes']
        print('Resumed optimizer step',start_step,flush=True)
    base={'run_id':run,'status':'running','config':config,'config_hash':config_hash,'model':lock,
          'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'processed_sha256':manifest['processed_sha256'],'order_manifest':str(order_path.relative_to(ROOT)),
          'trainable_parameters':model.get_nb_trainable_parameters()[0],'total_parameters':model.get_nb_trainable_parameters()[1],
          'planned_train_samples':len(set(order)),'planned_examples':len(order),
          'planned_sequence_tokens':order_record['sequence_tokens'],'planned_supervised_tokens':order_record['target_tokens'],
          'planned_optimizer_steps':steps,'adapter':str(dest.relative_to(ROOT)),
          'timing_note':'Train wall seconds includes step logs/checkpoints except final save; excludes load/preflight; resume excludes downtime'}
    base.update(history=history,train_seconds=prior_time,peak_allocated_bytes=prior_peak,peak_reserved_bytes=prior_reserved)
    def update_counts(completed_steps):
        seen=order[:min(completed_steps*accum,len(order))]
        base.update(train_samples=len(set(seen)),train_examples_seen=len(seen),
                    train_tokens_seen=sum(len(rows[i]['input_ids']) for i in seen),
                    supervised_tokens=sum(rows[i]['target_tokens'] for i in seen),optimizer_steps=completed_steps)
    update_counts(start_step)
    if checkpoint.exists():
        base['preflight_longest_sequence']=previous_report.get('preflight_longest_sequence')
        base['resume_history']=previous_report.get('resume_history',[])+[{
            'resumed_at_utc':datetime.now(timezone.utc).isoformat(),'checkpoint_step':start_step,
            'checkpoint_sha256':hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
            'previous_code_sha256':previous_report.get('code_sha256'),
            'previous_git_commit':previous_report.get('git_commit'),'note':args.resume_note,
            'discarded_completed_step_seconds':max(0,previous_report.get('train_seconds',prior_time)-prior_time),
            'unlogged_partial_step_seconds':'not measured; excluded from train_seconds'}]
    def sample_loss(row):
        ids=torch.tensor([row['input_ids']],device='cuda')
        # Causal shift: logits at position t-1 predict token t. Masked prompt
        # logits need not be materialized through the 151936-wide vocabulary head.
        positions=torch.arange(row['prompt_tokens']-1,len(row['input_ids'])-1,device='cuda')
        with compute_context(quantization):
            logits=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=False,logits_to_keep=positions).logits
        targets=ids[:,row['prompt_tokens']:]
        return F.cross_entropy(logits.float().reshape(-1,logits.shape[-1]),targets.reshape(-1))
    if not checkpoint.exists():
        before=torch.get_rng_state();cuda_before=torch.cuda.get_rng_state_all()
        probe=rows[max(range(len(rows)),key=lambda i:len(rows[i]['input_ids']))]
        try:
            loss=sample_loss(probe);loss.backward()
        except BaseException:
            base.update(status='failed_preflight',error=traceback.format_exc())
            report.write_text(json.dumps(base,indent=2)+'\n');raise
        assert torch.isfinite(loss) and any(p.grad is not None and p.grad.abs().sum()>0 for p in params)
        optimizer.zero_grad(set_to_none=True)
        del loss
        torch.set_rng_state(before);torch.cuda.set_rng_state_all(cuda_before)
        base['preflight_longest_sequence']=len(probe['input_ids'])
        print('Longest-sequence backward passed',len(probe['input_ids']),flush=True)
    torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
    try:
        for step in range(start_step,steps):
            batch_indices=order[step*accum:(step+1)*accum]
            warm=config['warmup_steps']
            scale=(step+1)/warm if step<warm else .5*(1+math.cos(math.pi*(step-warm)/max(1,steps-warm)))
            for group in optimizer.param_groups:group['lr']=config['learning_rate']*scale
            optimizer.zero_grad(set_to_none=True);total_loss=0.;total_objective=0.
            for i in batch_indices:
                loss=sample_loss(rows[i])
                if not torch.isfinite(loss):raise RuntimeError(f'Nonfinite loss on train:{i}')
                total_loss+=loss.detach().item()
                objective=loss*loss_weights[i]
                total_objective+=objective.detach().item();(objective/len(batch_indices)).backward()
            norm=torch.nn.utils.clip_grad_norm_(params,config['max_grad_norm'])
            if not torch.isfinite(norm):raise RuntimeError('Nonfinite gradient norm')
            optimizer.step();torch.cuda.synchronize()
            elapsed=prior_time+time.perf_counter()-start
            peak=max(prior_peak,torch.cuda.max_memory_allocated());reserved=max(prior_reserved,torch.cuda.max_memory_reserved())
            history.append({'step':step+1,'loss':total_loss/len(batch_indices),'weighted_objective':total_objective/len(batch_indices),'lr':optimizer.param_groups[0]['lr'],
                            'grad_norm':float(norm),'elapsed_seconds':elapsed,'examples_seen':min((step+1)*accum,len(order))})
            if (step+1)%5==0 or step==start_step:
                print(run,step+1,'/',steps,'loss',round(history[-1]['loss'],4),'seconds',round(elapsed,1),flush=True)
            base.update(history=history,train_seconds=elapsed,peak_allocated_bytes=peak,peak_reserved_bytes=reserved)
            update_counts(step+1)
            report.write_text(json.dumps(base,indent=2)+'\n')
            if (step+1)%config['checkpoint_every_steps']==0 or step+1==steps:
                checkpoint.parent.mkdir(parents=True,exist_ok=True)
                state={'config_hash':config_hash,'step':step+1,'adapter':get_peft_model_state_dict(model),
                       'optimizer':optimizer.state_dict(),'history':history,'cpu_rng':torch.get_rng_state(),
                       'cuda_rng':torch.cuda.get_rng_state_all(),'train_seconds':elapsed,
                       'peak_allocated_bytes':peak,'peak_reserved_bytes':reserved}
                temporary=checkpoint.with_suffix('.tmp');torch.save(state,temporary);temporary.replace(checkpoint)
        dest.mkdir(parents=True,exist_ok=True);model.save_pretrained(dest)
        base.update(status='completed',adapter_sha256=hashlib.sha256((dest/'adapter_model.safetensors').read_bytes()).hexdigest())
        report.write_text(json.dumps(base,indent=2)+'\n')
        print('Training completed',run,flush=True)
    except BaseException:
        base.update(status='failed',error=traceback.format_exc(),history=history)
        report.write_text(json.dumps(base,indent=2)+'\n');raise


if __name__=='__main__':main()
