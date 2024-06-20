def func():
    # Implement your logic here
    def evaluate_regression_models(models, X_test, y_test, weights=None):
        from sklearn.metrics import mean_squared_error, mean_absolute_error
        import numpy as np
        import pandas as pd
    
        evaluation_metrics = {}
        best_score = np.inf  # Initialize with infinity as we aim to minimize the scores
    
        for i, model in enumerate(models):
            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            
            # Calculate combined score with weights if provided
            if weights:
                combined_score = sum([weight * metric for weight, metric in zip(weights.values(), [rmse, mse, mae])])
            else:
                # Equal weights for all metrics if weights are not provided
                default_weights = {'RMSE': 0.33, 'MSE': 0.33, 'MAE': 0.33}
                combined_score = sum([weight * metric for weight, metric in zip(default_weights.values(), [rmse, mse, mae])])
    
            evaluation_metrics[f'Model_{i+1}'] = {'RMSE': rmse, 'MSE': mse, 'MAE': mae}
            evaluation_metrics[f'Model_{i+1}']['Combined_Score'] = combined_score
            evaluation_metrics[f'Model_{i+1}']['Model_Name'] = str(model)
    
            if combined_score < best_score:
                best_score = combined_score
                best_model = model
    
        return best_model, evaluation_metrics

    return evaluate_regression_models

evaluate_regression_models = func()