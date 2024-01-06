import json
from userInput.process_user_input import process_user_input  

def evaluate_model_accuracy(test_data_path, merge_threshold=-0.6):
    with open(test_data_path, 'r') as file:
        test_data = json.load(file)

    correct_predictions = 0
    baseline_correct_predictions = 0
    total_predictions = 0

    for repo, functions in test_data.items():
        for function_key, function_data in functions.items():
            merged_function = function_data['merged_function']
            actual_decision = "🎉 Merge the function 🎉" if function_data['score'] <= merge_threshold else "🙅 Do not merge the function 🙅"
            predicted_decision = process_user_input(merged_function)

            # Update correct predictions for the model
            if predicted_decision == actual_decision:
                correct_predictions += 1

            # Update correct predictions for the baseline (always predict "🎉 Merge the function 🎉")
            if actual_decision == "🎉 Merge the function 🎉":
                baseline_correct_predictions += 1

            total_predictions += 1
            print(f"Actual: {actual_decision}, Predicted: {predicted_decision}")

    # Calculate accuracies
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    baseline_accuracy = baseline_correct_predictions / total_predictions if total_predictions > 0 else 0

    return accuracy, baseline_accuracy

if __name__ == '__main__':
    accuracy, baseline_accuracy = evaluate_model_accuracy('./dataForTesting/testing.json')
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print(f"Baseline Accuracy: {baseline_accuracy * 100:.2f}%")