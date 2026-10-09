"""Explicit base loading policies; quantized runs cannot silently use BF16 weights."""
from contextlib import nullcontext


def load_base(path, quantization='none'):
    import torch
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig
    options = dict(local_files_only=True, dtype=torch.bfloat16,
                   device_map={'': 'cuda:0'}, attn_implementation='sdpa')
    if quantization == 'nf4_double':
        options['quantization_config'] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16)
    elif quantization != 'none':
        raise ValueError(f'Unsupported quantization policy: {quantization}')
    model = AutoModelForCausalLM.from_pretrained(path, **options)
    if quantization == 'nf4_double':
        from peft import prepare_model_for_kbit_training
        # Apply the SAME nonquantized-parameter dtype policy at train and inference.
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=False)
        assert model.is_loaded_in_4bit
    return model


def compute_context(quantization='none'):
    if quantization == 'none':
        return nullcontext()
    if quantization != 'nf4_double':
        raise ValueError(quantization)
    import torch
    return torch.autocast('cuda', dtype=torch.bfloat16)
