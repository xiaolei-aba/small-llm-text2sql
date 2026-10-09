"""Fixed train-only per-example objective weights, normalized over exposures."""
import math


def normalized_loss_weights(rows, order, difficulty_weights=None):
    if difficulty_weights is None:
        return [1.0] * len(rows)
    raw = [float(difficulty_weights[row['difficulty']]) for row in rows]
    if not order or any(not math.isfinite(w) or w <= 0 for w in raw):
        raise ValueError('Loss weights and training exposures must be positive and finite')
    mean = sum(raw[i] for i in order) / len(order)
    return [w / mean for w in raw]
