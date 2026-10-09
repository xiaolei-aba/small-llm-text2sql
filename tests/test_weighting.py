import unittest
import torch
from src.train.weighting import normalized_loss_weights


class WeightingTests(unittest.TestCase):
    def test_uniform_preserves_objective_and_gradient(self):
        rows = [{'difficulty': d} for d in ['easy', 'hard', 'medium']]
        for mapping in [None, {'easy': 1, 'medium': 1, 'hard': 1}]:
            weights = normalized_loss_weights(rows, [2, 0, 1], mapping)
            x = torch.tensor([.4, .7, .2], requires_grad=True)
            baseline = (x.square().sum() / 3)
            weighted = sum(w * t.square() for w, t in zip(weights, x)) / 3
            self.assertEqual(baseline.item(), weighted.item())
            self.assertTrue(torch.equal(torch.autograd.grad(baseline, x)[0],
                                        torch.autograd.grad(weighted, x)[0]))

    def test_mean_one_and_relative_ratio(self):
        rows = [{'difficulty': d} for d in ['easy', 'hard', 'hard']]
        weights = normalized_loss_weights(rows, [2, 0, 1], {'easy': 1, 'hard': 2})
        self.assertAlmostEqual(sum(weights) / 3, 1)
        self.assertAlmostEqual(weights[1] / weights[0], 2)

    def test_reject_invalid(self):
        for value in [0, -1, float('nan'), float('inf')]:
            with self.assertRaises(ValueError):
                normalized_loss_weights([{'difficulty': 'easy'}], [0], {'easy': value})


if __name__ == '__main__':
    unittest.main()
