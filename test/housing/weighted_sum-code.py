def func(weights, scores):
    # Implement your logic here
    weighted_sum = sum(w * s for w, s in zip(weights, scores))
    return weighted_sum


combined_score = func(weights, scores)
