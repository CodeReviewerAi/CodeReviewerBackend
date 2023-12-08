"""
How to improve this Code:
1. Account for functions that are renamed
2. Account for functions with the same name but different bodies
3. Filter comment and whitespace changes
4. Start increasing the number of commits only after the first merge commit
5. Use a more sophisticated hashing algorithm
6. Use a more sophisticated regular expression to match function declarations and bodies
7. Add more tests
8. Write the full function along with the commit into a json file
"""
import subprocess
import re
import json
from hashlib import sha256

def get_js_commits(repo_path):
    command = ["git", "-C", repo_path, "log", "--pretty=format:%H", "--", "*.js"]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')

def get_commit_diff(repo_path, commit_hash):
    command = ["git", "-C", repo_path, "show", commit_hash, "--", "*.js"]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout

def extract_functions(diff):
    # Regular expression to match the function declarations and bodies in the format: 'function <name>(<args>) {<body>}'
    function_regex = r"function\s+([a-zA-Z_$][0-9a-zA-Z_$]*)\s*\([^)]*\)\s*\{[\s\S]*?\}"
    return re.findall(function_regex, diff)

def hash_function_body(function_body):
    return sha256(function_body.encode('utf-8')).hexdigest()

def analyze_commits(repo_path, commits):
    function_changes = {}

    for commit in reversed(commits):  # Reverse the commit list to start from the earliest commit
        diff = get_commit_diff(repo_path, commit)
        functions = extract_functions(diff)

        for function_name in functions:
            full_function = 'function ' + function_name + diff.split(function_name)[1].split('}')[0] + '}'

            function_hash = hash_function_body(full_function)

            if function_name not in function_changes:
                # Store the first version of the function and initialize the count and hash set
                function_changes[function_name] = {
                    'count': 0,
                    'hashes': set(),
                    'first_version': full_function  # Store the first version of the function
                }

            if function_hash not in function_changes[function_name]['hashes']:
                function_changes[function_name]['count'] += 1
                function_changes[function_name]['hashes'].add(function_hash)

    return function_changes

def main():
    repo_path = './inputData/walgreens'
    commits = get_js_commits(repo_path)
    function_changes = analyze_commits(repo_path, commits)

    # Prepare data for JSON output
    output_data = {function_name: {'count': data['count'], 'first_version': data['first_version']} 
                   for function_name, data in function_changes.items()}

    # Write to JSON file
    with open('./outputData/function_changes.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    for function_name, data in function_changes.items():
        print(f"Function '{function_name}' changed {data['count']} times")

if __name__ == "__main__":
    main()

