import unittest
import json
import os
import sys

sys.path.append('../')
import getFunctionData

class TestFunctionData(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_createdWithMergeAndNotChanged(self):
        # Execute the script to update the function data
        getFunctionData.get_function_data()

        # Load the function changes data
        with open('./outputData/function_changes.json', 'r') as file:
            function_data = json.load(file)

        # Define the expected function key and content
        expected_key = 'blocks/cards/cards.js::createdWithMergeAndNotChanged'
        expected_function = {
            'function_name': 'createdWithMergeAndNotChanged',
            'merged_function': 'function createdWithMergeAndNotChanged() {\n  // this creates the function a branch other than main\n  // this is the first change in the test branch\n}',
            'changes_after_merge': 0
        }

        # Check if the function data contains the expected function with the correct data
        self.assertIn(expected_key, function_data)
        self.assertEqual(function_data[expected_key]['function_name'], expected_function['function_name'])
        self.assertEqual(function_data[expected_key]['merged_function'], expected_function['merged_function'])
        self.assertEqual(function_data[expected_key]['changes_after_merge'], expected_function['changes_after_merge'])

class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super(CustomTestRunner, self).run(test)
        if result.wasSuccessful():
            # ANSI escape code for green text
            print("\033[92m" + "All tests passed successfully!" + "\033[0m 🚀 🚀 🚀")
        return result

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())
