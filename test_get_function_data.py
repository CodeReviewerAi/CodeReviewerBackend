import unittest
import json
import sys

sys.path.append('../')
import getFunctionData

class TestFunctionData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Execute the script to update the function data
        getFunctionData.get_function_data()

        # Load the function changes data
        with open('./outputData/test_function_changes.json', 'r') as file:
            cls.function_data = json.load(file)

    def test_createdWithMergeAndNotChangedAfter(self):
        # Define the expected function key and content
        expected_key = 'blocks/test.js::createdWithMergeAndNotChangedAfter'
        expected_function = {
            'function_name': 'createdWithMergeAndNotChangedAfter',
            'merged_function': "function createdWithMergeAndNotChangedAfter() {\n    console.log('This creates the function on test branch')\n    console.log('Second change on test branch')\n}",
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

    """
    def test_CreatedOnMainAndNotChangedAfterMerge(self):
        # Define the expected function key and content
        expected_key = 'blocks/test.js::CreatedOnMainAndNotChangedAfterMerge'
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
        expected_key = 'blocks/test.js::createdWithMergeAndChangedAfterMerge'
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
        
    def test_createdOnMainAndChangedAfterMerge(self):
        # Define the expected function key and content
        expected_key = 'blocks/test.js::createdOnMainAndChangedAfterMerge'
        expected_function = {
            'function_name': 'createdOnMainAndChangedAfterMerge',
            'merged_function': 'function createdOnMainAndChangedAfterMerge() {\n    first change on main\n    change on test branch\n    second change on test branch\n}',
            'changes_after_merge': 1
        }

        # Check if the function data contains the expected function with the correct data
        self.assertIn(expected_key, self.function_data)
        self.assertEqual(self.function_data[expected_key]['function_name'], expected_function['function_name'])
        self.assertEqual(self.function_data[expected_key]['merged_function'].strip(), expected_function['merged_function'].strip())
        self.assertEqual(self.function_data[expected_key]['changes_after_merge'], expected_function['changes_after_merge'])
        
    def test_changedAfterMergeWithMerge(self):
        # Define the expected function key and content
        expected_key = 'blocks/test.js::changedAfterMergeWithMerge'
        expected_function = {
            'function_name': 'changedAfterMergeWithMerge',
            'merged_function': 'function changedAfterMergeWithMerge() {\n    this is the first change\n    this is the second change\n}',
            'changes_after_merge': 2
        }

        # Check if the function data contains the expected function with the correct data
        self.assertIn(expected_key, self.function_data)
        self.assertEqual(self.function_data[expected_key]['function_name'], expected_function['function_name'])
        self.assertEqual(self.function_data[expected_key]['merged_function'].strip(), expected_function['merged_function'].strip())
        self.assertEqual(self.function_data[expected_key]['changes_after_merge'], expected_function['changes_after_merge'])
    """ 
class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super(CustomTestRunner, self).run(test)
        if result.wasSuccessful():
            # ANSI escape code for green text
            print("\033[92m" + "All tests passed successfully!" + "\033[0m 🚀 🚀 🚀")
        return result

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())
