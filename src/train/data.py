"""SQL-only causal supervision; never silently truncate a schema or answer."""
from src.data.prompt import messages


def encode_example(tokenizer, question, schema, sql, max_length):
    prompt = tokenizer.apply_chat_template(messages(question, schema),
                                            tokenize=True, add_generation_prompt=True)
    full = tokenizer.apply_chat_template(messages(question, schema) +
                [{'role': 'assistant', 'content': sql}], tokenize=True,
                add_generation_prompt=False)
    if full[:len(prompt)] != prompt:
        raise ValueError('Chat template prefix changed at assistant boundary')
    # Include end-of-turn supervision, exclude template whitespace after it.
    end = full.index(tokenizer.eos_token_id, len(prompt)) + 1
    full = full[:end]
    if len(full) > max_length:
        raise ValueError(f'Sequence {len(full)} exceeds {max_length}; no truncation')
    labels = [-100] * len(prompt) + full[len(prompt):]
    if not any(x != -100 for x in labels):
        raise ValueError('Empty answer supervision')
    return {'input_ids': full, 'labels': labels, 'prompt_tokens': len(prompt),
            'target_tokens': len(full)-len(prompt)}


def collate(examples, pad_token_id):
    import torch
    size = max(len(e['input_ids']) for e in examples)
    return {
        'input_ids': torch.tensor([e['input_ids']+[pad_token_id]*(size-len(e['input_ids'])) for e in examples]),
        'attention_mask': torch.tensor([[1]*len(e['input_ids'])+[0]*(size-len(e['input_ids'])) for e in examples]),
        'labels': torch.tensor([e['labels']+[-100]*(size-len(e['labels'])) for e in examples]),
    }
