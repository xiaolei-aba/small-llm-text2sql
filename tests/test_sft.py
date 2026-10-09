import unittest
from pathlib import Path
from transformers import AutoTokenizer
from src.train.data import encode_example,collate


@unittest.skipUnless((Path(__file__).resolve().parents[1]/"models/Qwen2.5-Coder-1.5B-Instruct/tokenizer_config.json").is_file(),
                     "Official tokenizer is not distributed; download pinned tokenizer to run these 3 integration tests")
class SFTTokenizerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tok=AutoTokenizer.from_pretrained(Path(__file__).resolve().parents[1]/'models/Qwen2.5-Coder-1.5B-Instruct',local_files_only=True)

    def test_answer_boundary(self):
        sql='SELECT COUNT(*) FROM t;'
        e=encode_example(self.tok,'Count rows','Table t: x INTEGER',sql,1024)
        n=e['prompt_tokens']
        self.assertEqual(e['labels'][:n],[-100]*n)
        self.assertEqual(e['labels'][n:],e['input_ids'][n:])
        self.assertEqual(e['labels'][-1],self.tok.eos_token_id)
        self.assertEqual(self.tok.decode(e['labels'][n:-1]),sql)

    def test_left_padded_batch_preserves_individual_chat_tokens(self):
        from src.data.prompt import messages
        conversations=[messages('Count rows.','Table t: x INTEGER'),
                       messages('List all values larger than three.','Table t: x INTEGER, y TEXT')]
        single=[self.tok.apply_chat_template(m,tokenize=True,add_generation_prompt=True) for m in conversations]
        texts=[self.tok.apply_chat_template(m,tokenize=False,add_generation_prompt=True) for m in conversations]
        old_side=self.tok.padding_side;old_pad=self.tok.pad_token_id
        try:
            self.tok.padding_side='left';self.tok.pad_token_id=self.tok.eos_token_id
            batch=self.tok(texts,add_special_tokens=False,padding=True,return_tensors='pt')
            for i,expected in enumerate(single):
                actual=batch['input_ids'][i][batch['attention_mask'][i].bool()].tolist()
                self.assertEqual(actual,expected)
                self.assertEqual(batch['attention_mask'][i,-1].item(),1)
        finally:
            self.tok.padding_side=old_side;self.tok.pad_token_id=old_pad

    def test_padding_and_overlength(self):
        a=encode_example(self.tok,'Count rows','Table t: x INTEGER','SELECT COUNT(*) FROM t;',1024)
        b=encode_example(self.tok,'List all values with a deliberately longer question','Table t: x INTEGER','SELECT x FROM t;',1024)
        batch=collate([a,b],self.tok.eos_token_id)
        for i,e in enumerate([a,b]):
            n=len(e['input_ids'])
            self.assertTrue((batch['labels'][i,n:]==-100).all())
            self.assertTrue((batch['attention_mask'][i,n:]==0).all())
            self.assertEqual(batch['labels'][i,n-1].item(),self.tok.eos_token_id)
        with self.assertRaisesRegex(ValueError,'no truncation'):
            encode_example(self.tok,'Count rows','Table t: x INTEGER','SELECT COUNT(*) FROM t;',10)


class SFTMathTests(unittest.TestCase):
    def test_selected_logits_loss_and_gradients_match_masked_loss(self):
        import torch
        import torch.nn.functional as F
        from transformers import Qwen2Config,Qwen2ForCausalLM
        torch.manual_seed(42)
        model=Qwen2ForCausalLM(Qwen2Config(vocab_size=32,hidden_size=16,intermediate_size=32,
                    num_hidden_layers=1,num_attention_heads=2,num_key_value_heads=2))
        model.eval()
        ids=torch.tensor([[1,2,3,4,5,6]])
        labels=ids.clone();labels[:,:3]=-100
        expected=model(input_ids=ids,labels=labels).loss
        expected.backward();grad=model.lm_head.weight.grad.clone();model.zero_grad()
        output=model(input_ids=ids,logits_to_keep=torch.arange(2,5)).logits
        actual=F.cross_entropy(output.reshape(-1,32),ids[:,3:].reshape(-1))
        actual.backward()
        torch.testing.assert_close(expected,actual)
        torch.testing.assert_close(grad,model.lm_head.weight.grad)

    def test_peft_checkpointed_selected_logits_backprop(self):
        import torch
        import torch.nn.functional as F
        from transformers import Qwen2Config,Qwen2ForCausalLM
        from peft import LoraConfig,get_peft_model
        base=Qwen2ForCausalLM(Qwen2Config(vocab_size=32,hidden_size=16,intermediate_size=32,
             num_hidden_layers=1,num_attention_heads=2,num_key_value_heads=2))
        model=get_peft_model(base,LoraConfig(r=2,lora_alpha=4,target_modules=['q_proj','v_proj'],task_type='CAUSAL_LM'))
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
        model.enable_input_require_grads();model.train()
        ids=torch.tensor([[1,2,3,4,5,6]])
        logits=model(input_ids=ids,use_cache=False,logits_to_keep=torch.arange(2,5)).logits
        F.cross_entropy(logits.reshape(-1,32),ids[:,3:].reshape(-1)).backward()
        self.assertTrue(any(p.grad is not None and p.grad.abs().sum()>0 for n,p in model.named_parameters() if 'lora_' in n))
        self.assertTrue(all(p.grad is None for n,p in model.named_parameters() if 'lora_' not in n))

    def test_adapter_optimizer_rng_resume_matches_uninterrupted_cpu(self):
        import io
        import torch
        from transformers import Qwen2Config,Qwen2ForCausalLM
        from peft import LoraConfig,get_peft_model,get_peft_model_state_dict,set_peft_model_state_dict
        def create():
            torch.manual_seed(42)
            base=Qwen2ForCausalLM(Qwen2Config(vocab_size=32,hidden_size=16,intermediate_size=32,
                 num_hidden_layers=1,num_attention_heads=2,num_key_value_heads=2))
            model=get_peft_model(base,LoraConfig(r=2,lora_alpha=4,lora_dropout=.2,
                    target_modules=['q_proj','v_proj'],task_type='CAUSAL_LM'))
            model.train()
            return model,torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=.001)
        def step(model,optimizer):
            ids=torch.tensor([[1,2,3,4,5,6]])
            labels=ids.clone();labels[:,:3]=-100
            optimizer.zero_grad(set_to_none=True)
            model(input_ids=ids,labels=labels,use_cache=False).loss.backward();optimizer.step()
        model,optimizer=create();step(model,optimizer)
        buffer=io.BytesIO()
        torch.save({'adapter':get_peft_model_state_dict(model),'optimizer':optimizer.state_dict(),
                    'rng':torch.get_rng_state()},buffer)
        step(model,optimizer)
        expected={k:v.clone() for k,v in get_peft_model_state_dict(model).items()}
        restored,new_optimizer=create();buffer.seek(0)
        state=torch.load(buffer,weights_only=False)
        set_peft_model_state_dict(restored,state['adapter']);new_optimizer.load_state_dict(state['optimizer'])
        torch.set_rng_state(state['rng']);step(restored,new_optimizer)
        for name,actual in get_peft_model_state_dict(restored).items():
            torch.testing.assert_close(actual,expected[name],rtol=0,atol=0)


if __name__=='__main__': unittest.main()
