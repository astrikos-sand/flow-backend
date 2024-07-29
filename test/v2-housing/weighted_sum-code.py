def func(weights, scores):
    # Implement your logic here
    weighted_sum = sum(w * s for w, s in zip(weights, scores))
    return weighted_sum


weighted_sum = func(weights, scores)
