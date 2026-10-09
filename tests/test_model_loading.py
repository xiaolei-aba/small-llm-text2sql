import unittest
from unittest.mock import patch
import torch
from src.utils.model_loading import load_base, compute_context


class ModelLoadingTests(unittest.TestCase):
    def test_unquantized_keeps_original_loading_options(self):
        with patch('transformers.AutoModelForCausalLM.from_pretrained') as load:
            model = load_base('local-model', 'none')
            load.assert_called_once_with('local-model', local_files_only=True,
                                         dtype=torch.bfloat16, device_map={'': 'cuda:0'},
                                         attn_implementation='sdpa')
            self.assertIs(model, load.return_value)
        with compute_context('none'):
            self.assertFalse(torch.is_autocast_enabled('cuda'))

    def test_unknown_quantization_is_not_silent_fallback(self):
        with patch('transformers.AutoModelForCausalLM.from_pretrained') as load:
            with self.assertRaises(ValueError):
                load_base('local-model', 'unknown-quantizer')
            load.assert_not_called()


if __name__ == '__main__':
    unittest.main()
