""" Things to consider
- How to handle API rate limits, should we instead save the repo locally?
- How to handle function with the same name in different files
- Should we use save the first function or the first function after the first merge commit?
- Should we consider only incrementing the value if 'fix' or 'bug' is in the commit message?
"""
import requests
import time
import os
import re
import json
import hashlib
from dotenv import load_dotenv

load_dotenv()

def fetch_all_commits(repo_api_url, headers):
    """ Fetch all commits from the repository """
    commits = []
    next_page_url = repo_api_url + '/commits'

    while next_page_url:
        response = requests.get(next_page_url, headers=headers)
        if response.status_code == 200:
            commits.extend(response.json())
            if 'next' in response.links:
                next_page_url = response.links['next']['url']
            else:
                break
        else:
            raise Exception(f'Failed to fetch commits: {response.status_code}')
    return commits

def extract_function_bodies_from_file(file_content):
    """ Extract entire function bodies from JavaScript file content """
    function_bodies = {}
    # Matches the start of the function and captures until the closing brace
    pattern = r'function\s+(\w+)\s*\(.*?\)\s*\{([\s\S]*?\n\})'
    matches = re.findall(pattern, file_content)

    for name, body in matches:
        # Create a hash of the function body
        hash_digest = hashlib.md5(body.encode()).hexdigest()
        function_bodies[name] = hash_digest

    return function_bodies

def analyze_commit_for_js_changes(commit_url, headers, prev_commit_functions={}):
    """ Analyze a specific commit for changes in JavaScript functions """
    function_changes = {}
    current_functions = {}  # Initialize current_functions
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        try:
            response = requests.get(commit_url, headers=headers)
            if response.status_code == 200:
                commit_data = response.json()
                for file in commit_data.get('files', []):
                    if file['filename'].endswith('.js'):
                        raw_url = file.get('raw_url', '')
                        file_content = requests.get(raw_url, headers=headers).text
                        current_functions = extract_function_bodies_from_file(file_content)
                        for func, hash_val in current_functions.items():
                            if func not in prev_commit_functions or prev_commit_functions[func] != hash_val:
                                function_changes[func] = function_changes.get(func, 0) + 1
            else:
                raise Exception(f'Failed to fetch commit details: {response.status_code}')
        except requests.exceptions.RequestException as e:
            attempt += 1
            time.sleep(2 ** attempt)
            print(f"Retrying ({attempt}/{max_attempts}) due to error: {e}")

    return function_changes, current_functions  # Return statement outside the try-except block

def main():
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}

    repo_api_url = 'https://api.github.com/repos/hlxsites/walgreens'

    try:
        commits = fetch_all_commits(repo_api_url, headers)
        overall_function_changes = {}
        prev_commit_functions = {}

        for commit in commits:
            commit_url = commit['url']
            function_changes, current_functions = analyze_commit_for_js_changes(commit_url, headers, prev_commit_functions)
            prev_commit_functions = current_functions
            for func, count in function_changes.items():
                overall_function_changes[func] = overall_function_changes.get(func, 0) + count

            # Print the changes for this commit
            print(f"Commit {commit['sha']}:")
            for func, count in function_changes.items():
                print(f"  - Function {func} changed {count} times")

        # After processing all commits, write the overall results to a file
        with open('function_changes.json', 'w') as file:
            json.dump(overall_function_changes, file, indent=4)

        print("Function change data written to function_changes.json")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()