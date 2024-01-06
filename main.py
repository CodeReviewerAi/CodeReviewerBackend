import unittest
import time
import json
import test_get_function_data
import function_data
#from userInput import evaluate_performance

def main(repos_info):
    for repo_info in repos_info:
        repo_path, data_type = repo_info['path'], repo_info['type']
        
        # Run the main function from getFunctionData
        print(f"Processing repository: {repo_path}, Data type: {data_type}")
        function_data_output = function_data.get_function_data(repo_path)

        # Output paths based on data type
        if data_type == 'training':
            output_path = './dataForTesting/training.json'
        elif data_type == 'testing':
            output_path = './dataForTesting/testing.json'
        else:  # Default to test
            output_path = './dataForTesting/test_function_changes.json'

        # Save function data to the appropriate file
        with open(output_path, 'w') as f:
            json.dump(function_data_output, f, indent=4)

    # Normalize the scores
    
    # Save the embeddings

    # Run the main function from processUserInput
    #evaluate_performance.main()

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromModule(test_get_function_data)

    # Run the tests with CustomTestRunner
    test_get_function_data.CustomTestRunner().run(suite)

if __name__ == '__main__':
    start_time = time.time()

    # List of repositories and their types
    repos_info = [
        {'path': '../inputData/testRepo', 'type': 'test'},
        # Add more repos here as needed, e.g.:
        # {'path': '../inputData/elixirsolutions', 'type': 'training'},
        # {'path': '../inputData/anotherRepo', 'type': 'testing'}
    ]

    main(repos_info)

    end_time = time.time()
    elapsed_time = round((end_time - start_time) / 60, 2)  # convert to minutes and round to 2 decimal places
    print(f'⏰ The program took {elapsed_time} minutes to run. ⏰')
