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

def analyze_commit_for_js_changes(commit_url, headers):
    """ Analyze a specific commit for changes in JavaScript functions """
    function_changes = {}
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        try:
            response = requests.get(commit_url, headers=headers)
            if response.status_code == 200:
                commit_data = response.json()
                for file in commit_data.get('files', []):
                    if file['filename'].endswith('.js'):
                        patch = file.get('patch', '')
                        functions_changed = extract_functions_from_patch(patch)
                        for func in functions_changed:
                            function_changes[func] = function_changes.get(func, 0) + 1
                return function_changes
            else:
                raise Exception(f'Failed to fetch commit details: {response.status_code}')
        except requests.exceptions.RequestException as e:
            attempt += 1
            time.sleep(2 ** attempt)  # Exponential backoff
            print(f"Retrying ({attempt}/{max_attempts}) due to error: {e}")

    raise Exception("Max retries reached")

def extract_functions_from_patch(patch):
    """ Extract function names from a commit patch """
    function_names = set()
    pattern = r'\+function (\w+)\s*\('
    matches = re.findall(pattern, patch)
    for match in matches:
        function_names.add(match)
    return function_names

def main():
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}

    repo_api_url = 'https://api.github.com/repos/hlxsites/bitdefender'

    try:
        commits = fetch_all_commits(repo_api_url, headers)
        overall_function_changes = {}

        for commit in commits:
            commit_url = commit['url']
            function_changes = analyze_commit_for_js_changes(commit_url, headers)
            for func, count in function_changes.items():
                overall_function_changes[func] = overall_function_changes.get(func, 0) + count
                print(f"Function {func} changed {count} times")

        # Convert the result to JSON and write to a file
        with open('function_changes.json', 'w') as file:
            json.dump(overall_function_changes, file, indent=4)

        print("Function change data written to function_changes.json")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
