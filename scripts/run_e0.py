"""Resumable batch-one zero-shot generation. Never use gold to build prompts."""
import argparse
import hashlib
import json
import os
import sys
import subprocess
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.data.schema import load_schema_index,format_schema
from src.data.prompt import messages
from src.inference.postprocess import extract_sql
from src.evaluation.safe_sql import execute


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--adapter')
    args=ap.parse_args()
    if Path(sys.prefix).name!='text2sql':
        raise RuntimeError('Use text2sql')
    import torch
    from transformers import AutoTokenizer
    from src.utils.model_loading import load_base,compute_context
    config=json.loads((ROOT/'configs/e0.json').read_text())
    lock=json.loads((ROOT/config['model_lock']).read_text())
    manifest=json.loads((ROOT/args.manifest).read_text())
    records=manifest['records']
    identity=[config,lock,manifest,args.adapter]
    adapter_hash=None;quantization='none'
    if args.adapter:
        adapter_hash=hashlib.sha256((ROOT/args.adapter/'adapter_model.safetensors').read_bytes()).hexdigest()
        training=json.loads((ROOT/'results'/f'{Path(args.adapter).name}_training.json').read_text())
        if training['status']!='completed' or training['adapter_sha256']!=adapter_hash:
            raise RuntimeError('Adapter does not match a completed training report')
        identity.append(adapter_hash)
        quantization=training['config'].get('quantization','none')
        if quantization!='none':identity.append(quantization)
    fingerprint=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    output=ROOT/args.output
    output.parent.mkdir(parents=True,exist_ok=True)
    done={}
    if output.exists():
        for line in output.read_text(encoding='utf-8').splitlines():
            row=json.loads(line)
            if row['config_hash']!=fingerprint:
                raise RuntimeError('Resume config mismatch')
            if row['sample_id'] in done:
                raise RuntimeError('Duplicate sample ID')
            done[row['sample_id']]=row
    todo=[r for r in records if r['sample_id'] not in done]
    if not todo:
        print('All manifest samples already saved; no inference repeated')
        return
    data=ROOT/'data/raw/spider/spider_data'
    dev=json.loads((data/'dev.json').read_text())
    schema_index=load_schema_index(data/'tables.json')
    schemas={db:format_schema(db,schema_index,data/'database'/db/(db+'.sqlite')) for db in sorted({r['db_id'] for r in todo})}
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError('BF16 CUDA unavailable; stop and investigate')
    torch.manual_seed(config['seed'])
    torch.cuda.reset_peak_memory_stats()
    start=time.perf_counter()
    tok=AutoTokenizer.from_pretrained(ROOT/lock['local_dir'],local_files_only=True)
    model=load_base(ROOT/lock['local_dir'],quantization)
    if args.adapter:
        from peft import PeftModel
        model=PeftModel.from_pretrained(model,ROOT/args.adapter)
    model.eval()
    torch.cuda.synchronize()
    profile={'loaded_at_utc':datetime.now(timezone.utc).isoformat(),'load_seconds':time.perf_counter()-start,
             'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'allocated_bytes':torch.cuda.memory_allocated(),'reserved_bytes':torch.cuda.memory_reserved(),
             'config_hash':fingerprint,'config':config,'model':lock,'adapter':args.adapter,'adapter_sha256':adapter_hash,
             'quantization':quantization}
    effective_quantization=getattr(model.config,'quantization_config',None)
    if effective_quantization is not None:
        profile['effective_quantization_config']=(effective_quantization.to_dict()
            if hasattr(effective_quantization,'to_dict') else effective_quantization)
    generate_kwargs=dict(do_sample=False,num_beams=1,max_new_tokens=config['max_new_tokens'],
                         pad_token_id=tok.eos_token_id)
    profile['effective_generation_config']={**model.generation_config.to_dict(),**generate_kwargs}
    # Fixed generic warmup contains no Spider answer.
    with torch.inference_mode(),compute_context(quantization):
        warm=tok.apply_chat_template(messages('Count rows in table t.','Table t: x INTEGER'),add_generation_prompt=True,return_tensors='pt').to('cuda')
        model.generate(warm,attention_mask=torch.ones_like(warm),do_sample=False,max_new_tokens=8,pad_token_id=tok.eos_token_id)
    torch.cuda.synchronize()
    profile_path=output.with_suffix('.profile.json')
    profile_path.write_text(json.dumps(profile,indent=2)+'\n')
    with output.open('a',encoding='utf-8') as stream:
        for record in todo:
            ex=dev[record['index']]
            row={**record,'question':ex['question'],'gold_sql':ex['query'],'config_hash':fingerprint}
            start=time.perf_counter()
            try:
                inputs=tok.apply_chat_template(messages(ex['question'],schemas[ex['db_id']]),
                      tokenize=True,add_generation_prompt=True,return_tensors='pt',return_dict=True).to('cuda')
                n=inputs['input_ids'].shape[1]
                if n>config['max_input_tokens']:
                    raise ValueError(f'Input budget exceeded: {n}; no silent truncation')
                with torch.inference_mode(),compute_context(quantization):
                    generated=model.generate(**inputs,**generate_kwargs)[0,n:]
                torch.cuda.synchronize()
                raw=tok.decode(generated,skip_special_tokens=True)
                eos=model.generation_config.eos_token_id
                eos_ids=set(eos if isinstance(eos,list) else [eos])
                ended_on_eos=bool(len(generated) and int(generated[-1]) in eos_ids)
                row.update(raw_output=raw,generated_sql=extract_sql(raw),prompt_tokens=n,
                           generated_tokens=len(generated),generation_time=time.perf_counter()-start,
                           generation_status='ok',ended_on_eos=ended_on_eos,
                           truncated=len(generated)==config['max_new_tokens'] and not ended_on_eos)
                result=execute(row['generated_sql'],data/'database'/ex['db_id']/(ex['db_id']+'.sqlite'))
                row.update(execution_success=result['ok'],execution_error=result['error'])
            except torch.cuda.OutOfMemoryError:
                profile['fatal_error']=traceback.format_exc()
                profile_path.write_text(json.dumps(profile,indent=2)+'\n')
                raise
            except Exception:
                row.update(raw_output='',generated_sql='',prompt_tokens=record['prompt_tokens'],generated_tokens=0,
                           generation_time=time.perf_counter()-start,generation_status='failed',
                           execution_success=False,execution_error=traceback.format_exc())
            row['peak_allocated_bytes']=torch.cuda.max_memory_allocated()
            row['peak_reserved_bytes']=torch.cuda.max_memory_reserved()
            stream.write(json.dumps(row,ensure_ascii=False)+'\n'); stream.flush(); os.fsync(stream.fileno())
            print(row['sample_id'],row['generation_status'],row['generated_tokens'],round(row['generation_time'],2),flush=True)
    profile.update(peak_allocated_bytes=torch.cuda.max_memory_allocated(),peak_reserved_bytes=torch.cuda.max_memory_reserved())
    profile_path.write_text(json.dumps(profile,indent=2)+'\n')


if __name__=='__main__':
    main()
