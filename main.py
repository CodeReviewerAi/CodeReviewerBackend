import time
import json
import function_data
import normalize_scores
import embed_training_data
import evaluate_performance
from userInput.process_user_input import process_user_input 

def main(repos_info):
    for repo_info in repos_info:
        repo_path, data_type = repo_info['path'], repo_info['type']
        
        # Run the main function from getFunctionData
        print(f"Processing repository: {repo_path}, Data type: {data_type}")
        function_data_output = function_data.get_function_data(repo_path)

        # Output paths based on data type
        if data_type == 'training':
            output_path = './dataForTesting/training.json'
        else:  # Default to test
            output_path = './dataForTesting/testing.json'

        # Save function data to the appropriate file
        with open(output_path, 'w') as f:
            json.dump(function_data_output, f, indent=4)

    # Normalize the scores for all data
    normalize_scores.normalize_and_save_change_counts('dataForTesting/training.json')
    normalize_scores.normalize_and_save_change_counts('dataForTesting/testing.json')
    print("Done normalizing scores")
   
    # Load the function data from the file
    with open('dataForTesting/training.json', 'r') as f:
        training_data = json.load(f)

    # Save the embeddings
    embed_training_data.embed_repos_functions(training_data)
    
    # Get the performance metrics
    accuracy, baseline_accuracy = evaluate_performance.evaluate_model_accuracy('./dataForTesting/testing.json')
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print(f"Baseline Accuracy: {baseline_accuracy * 100:.2f}%")

if __name__ == '__main__':    
    start_time = time.time()

    # List of repositories and their types
    repos_info = [
        {'path': '../inputData/trainingData/24petwatch', 'type': 'training'},
        {'path': '../inputData/trainingData/danaher-ls-aem', 'type': 'training'},
        {'path': '../inputData/trainingData/mammotome', 'type': 'training'},
        {'path': '../inputData/trainingData/moleculardevices', 'type': 'training'},
        {'path': '../inputData/trainingData/petplace', 'type': 'training'},
        {'path': '../inputData/trainingData/theplayers', 'type': 'training'},
        {'path': '../inputData/trainingData/walgreens', 'type': 'training'},
        {'path': '../inputData/testData/elixirsolutions', 'type': 'testing'},
    ]

    main(repos_info)

    end_time = time.time()
    elapsed_time = round((end_time - start_time) / 60, 2)  # convert to minutes and round to 2 decimal places
    print(f'⏰ The program took {elapsed_time} minutes to run. ⏰')
