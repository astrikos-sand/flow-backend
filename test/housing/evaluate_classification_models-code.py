def func():
    # Implement your logic here
    def evaluate_classification_models(models, X_test, y_test, weights=None):
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        import pandas as pd
    
        evaluation_metrics = {}
        best_score = 0
        best_model = models[0]  # Default to first model if no better model found
        
        for i, model in enumerate(models):
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='macro')
            recall = recall_score(y_test, y_pred, average='macro')
            f1 = f1_score(y_test, y_pred, average='macro')
            
            # Calculate combined score with weights if provided
            if weights:
                combined_score = sum([weight * metric for weight, metric in zip(weights.values(), [accuracy, precision, recall, f1])])
            else:
                # Equal weights for all metrics if weights are not provided
                default_weights = {'Accuracy': 0.25, 'Precision': 0.25, 'Recall': 0.25, 'F1-Score': 0.25}
                combined_score = sum([weight * metric for weight, metric in zip(default_weights.values(), [accuracy, precision, recall, f1])])
                
                
            evaluation_metrics[f'Model_{i+1}'] = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1-Score': f1}
            evaluation_metrics[f'Model_{i+1}']['Combined_Score'] = combined_score
            evaluation_metrics[f'Model_{i+1}']['Model_Name'] = str(model)
            
            if combined_score > best_score:
                best_score = combined_score
                best_model = model
        
        if best_score == 0:
            print("All models having a combined score of 0:")
            print("- Data size is too small, resulting in one class dominating or missing, leading to the above issues. It's suggested to acquire a proper dataset.")
    
        return best_model, evaluation_metrics

    return evaluate_classification_models

evaluate_classification_models = func()