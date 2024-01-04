import unittest
import time
import test_get_function_data
import getFunctionData
import createEmbeddings
from userInput import processUserInput

def main(repo_path='../inputData/testRepo'):
    # Run the main function from getFunctionData
    getFunctionData.get_function_data(repo_path)

    # Run the main function from createEmbeddings
    createEmbeddings.embed_sample_functions(repo_path)

    # Run the main function from processUserInput
    processUserInput.process_user_input()

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromModule(test_get_function_data)

    # Run the tests with CustomTestRunner
    test_get_function_data.CustomTestRunner().run(suite)

if __name__ == '__main__':
    start_time = time.time()
     # pass this variable if you want to run another repo than testRepo: 
     # repo_path='../inputData/elixirsolutions'
    main()
    end_time = time.time()
    elapsed_time = round((end_time - start_time) / 60, 2)  # convert to minutes and round to 2 decimal places
    print(f'⏰ The program took {elapsed_time} minutes to run. ⏰')