"""Post-E3 native NF4 compatibility/resource probe; weights never used for evaluation."""
import gc
import hashlib
import json
import random
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    if Path(sys.prefix).name != 'text2sql':
        raise RuntimeError('Use text2sql')
    if not (ROOT / 'results/e3_dev_summary.json').exists():
        raise RuntimeError('Finish core E3 before optional E4 GPU probe')
    target = ROOT / 'results/e4_compatibility_probe.json'
    if target.exists():
        raise RuntimeError('Preserve previous probe evidence; inspect before rerun')
    report = {'status': 'running', 'observed_at_utc': datetime.now(timezone.utc).isoformat(),
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'note': 'Discarded compatibility/short timing probe; no full-training accuracy or throughput claim'}
    target.write_text(json.dumps(report, indent=2) + '\n')
    try:
        import torch
        import torch.nn.functional as F
        import bitsandbytes as bnb
        from peft import LoraConfig, get_peft_model
        from src.utils.model_loading import load_base, compute_context
        report.update(torch=torch.__version__, bitsandbytes=bnb.__version__)
        assert bnb.__version__ == '0.47.0'
        torch.manual_seed(42)
        layer = bnb.nn.Linear4bit(64, 64, bias=False, compute_dtype=torch.bfloat16,
                                 compress_statistics=True, quant_type='nf4').to('cuda')
        x = torch.randn(4, 64, device='cuda', dtype=torch.bfloat16, requires_grad=True)
        layer(x).float().square().mean().backward()
        assert torch.isfinite(x.grad).all()
        report['nf4_linear_backward'] = 'passed'
        del layer, x
        gc.collect(); torch.cuda.empty_cache()
        cfg = json.loads((ROOT / 'configs/e4.json').read_text())
        lock = json.loads((ROOT / 'configs/model_lock.json').read_text())
        rows = [json.loads(line) for line in (ROOT / 'data/processed/sft_train.jsonl').read_text().splitlines()]
        order = list(range(len(rows))); random.Random(cfg['seed']).shuffle(order)
        assert order == json.loads((ROOT / cfg['control_order_manifest']).read_text())['indices']
        torch.manual_seed(cfg['seed']); torch.cuda.manual_seed_all(cfg['seed'])
        model = load_base(ROOT / lock['local_dir'], 'nf4_double')
        model.config.use_cache = False
        model = get_peft_model(model, LoraConfig(r=cfg['rank'], lora_alpha=cfg['alpha'],
                lora_dropout=cfg['dropout'], target_modules=cfg['target_modules'], bias='none', task_type='CAUSAL_LM'))
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
        model.enable_input_require_grads(); model.train()
        params = [p for p in model.parameters() if p.requires_grad]
        assert all('lora_' in n for n, p in model.named_parameters() if p.requires_grad)
        opt = torch.optim.AdamW(params, lr=cfg['learning_rate'], weight_decay=cfg['weight_decay'])

        def loss(row):
            ids = torch.tensor([row['input_ids']], device='cuda')
            positions = torch.arange(row['prompt_tokens'] - 1, len(row['input_ids']) - 1, device='cuda')
            with compute_context('nf4_double'):
                logits = model(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False,
                               logits_to_keep=positions).logits
            return F.cross_entropy(logits.float().reshape(-1, logits.shape[-1]), ids[:, row['prompt_tokens']:].reshape(-1))

        longest = max(rows, key=lambda r: len(r['input_ids']))
        value = loss(longest); value.backward()
        assert torch.isfinite(value) and any(p.grad is not None and p.grad.abs().sum() > 0 for p in params)
        opt.zero_grad(set_to_none=True); del value
        report['longest_sequence_backward'] = len(longest['input_ids'])
        torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
        durations = []
        for step in range(5):
            start = time.perf_counter()
            for group in opt.param_groups:
                group['lr'] = cfg['learning_rate'] * (step + 1) / cfg['warmup_steps']
            opt.zero_grad(set_to_none=True)
            for index in order[step * 16:(step + 1) * 16]:
                value = loss(rows[index]); assert torch.isfinite(value)
                (value / 16).backward()
            norm = torch.nn.utils.clip_grad_norm_(params, cfg['max_grad_norm'])
            assert torch.isfinite(norm)
            opt.step(); torch.cuda.synchronize()
            durations.append(time.perf_counter() - start)
            print('Discarded QLoRA probe step', step + 1, durations[-1], flush=True)
        report.update(status='passed', step_seconds=durations, probe_examples=80,
                      rough_full_train_minutes=sum(durations) / len(durations) * 438 / 60,
                      peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                      peak_reserved_bytes=torch.cuda.max_memory_reserved(),
                      trainable_parameters=model.get_nb_trainable_parameters()[0])
        target.write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
    except BaseException:
        report.update(status='failed', error=traceback.format_exc())
        target.write_text(json.dumps(report, indent=2) + '\n')
        raise


if __name__ == '__main__':
    main()
