import unittest
import json
import sys

sys.path.append('../')
import getFunctionData

class TestFunctionData(unittest.TestCase):

    def setUp(self):
        # Execute the script to update the function data
        getFunctionData.get_function_data()

        # Load the function changes data
        with open('./outputData/function_changes.json', 'r') as file:
            self.function_data = json.load(file)

    def test_createdWithMergeAndNotChangedAfter(self):
        # Define the expected function key and content
        expected_key = 'blocks/tests.js::createdWithMergeAndNotChangedAfter'
        expected_function = {
            'function_name': 'createdWithMergeAndNotChangedAfter',
            'merged_function': 'function createdWithMergeAndNotChangedAfter() {\n    This is the first change\n    This is the second change\n}',
            'changes_after_merge': 0
        }

        # Check if the function data contains the expected function with the correct data
        self.assertIn(expected_key, self.function_data)
        self.assertEqual(self.function_data[expected_key]['function_name'], expected_function['function_name'])

        # Check if the function data contains the expected function with the correct data
        self.assertIn(expected_key, self.function_data)
        self.assertEqual(self.function_data[expected_key]['function_name'], expected_function['function_name'])
        self.assertEqual(self.function_data[expected_key]['merged_function'].strip(), expected_function['merged_function'].strip())
        self.assertEqual(self.function_data[expected_key]['changes_after_merge'], expected_function['changes_after_merge'])

    def test_CreatedOnMainAndNotChangedAfterMerge(self):
        # Define the expected function key and content
        expected_key = 'blocks/tests.js::CreatedOnMainAndNotChangedAfterMerge'
        expected_function = {
            'function_name': 'CreatedOnMainAndNotChangedAfterMerge',
            'merged_function': 'function CreatedOnMainAndNotChangedAfterMerge() {\n    this is the first change\n    this is the second change\n    this is the third change\n}',
            'changes_after_merge': 0
        }

        # Check if the function data contains the expected function with the correct data
        self.assertIn(expected_key, self.function_data)
        self.assertEqual(self.function_data[expected_key]['function_name'], expected_function['function_name'])
        self.assertEqual(self.function_data[expected_key]['merged_function'].strip(), expected_function['merged_function'].strip())
        self.assertEqual(self.function_data[expected_key]['changes_after_merge'], expected_function['changes_after_merge'])
    
    def test_createdWithMergeAndChangedAfterMerge(self):
        # Define the expected function key and content
        expected_key = 'blocks/tests.js::createdWithMergeAndChangedAfterMerge'
        expected_function = {
            'function_name': 'createdWithMergeAndChangedAfterMerge',
            'merged_function': 'function createdWithMergeAndChangedAfterMerge() {\n    this is the first change\n    this is the second change\n}',
            'changes_after_merge': 1
        }

        # Check if the function data contains the expected function with the correct data
        self.assertIn(expected_key, self.function_data)
        self.assertEqual(self.function_data[expected_key]['function_name'], expected_function['function_name'])
        self.assertEqual(self.function_data[expected_key]['merged_function'].strip(), expected_function['merged_function'].strip())
        self.assertEqual(self.function_data[expected_key]['changes_after_merge'], expected_function['changes_after_merge'])
        
class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super(CustomTestRunner, self).run(test)
        if result.wasSuccessful():
            # ANSI escape code for green text
            print("\033[92m" + "All tests passed successfully!" + "\033[0m 🚀 🚀 🚀")
        return result

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())
