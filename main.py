import unittest
import test_get_function_data
import getFunctionData
import createEmbeddings
from userInput import processUserInput

# Run the main function from getFunctionData
getFunctionData.get_function_data()

# Run the main function from createEmbeddings
createEmbeddings.embed_sample_functions()

# Run the main function from processUserInput
processUserInput.process_user_input()

# Create a test suite
suite = unittest.TestLoader().loadTestsFromModule(test_get_function_data)

# Run the tests with CustomTestRunner
test_get_function_data.CustomTestRunner().run(suite)