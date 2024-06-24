def func(models, scores):
    # Implement your logic here
    model_score_pairs = zip(models, scores)

    # Initialize variables to track the best model and its score
    best_model = None
    best_score = -float("inf")  # Initialize with a very low score

    # Iterate through each model and score pair
    for model, score in model_score_pairs:
        # Check if the current model has a higher score than the best found so far
        if score > best_score:
            best_score = score
            best_model = model
    return best_model


best_model = func(models, scores)
