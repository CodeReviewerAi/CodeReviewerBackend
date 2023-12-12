import git
import json
import re

# Path to your repository
repo_path = '../inputData/testRepo2'
repo = git.Repo(repo_path)

merge_commits = [commit for commit in repo.iter_commits('main') if commit.parents and len(commit.parents) > 1]
merge_commits.reverse() # Reverse the list to get the oldest merge commit first 

def extract_js_functions(diff):
    # Regular expression to match JavaScript function declarations
    # This regex can be adjusted based on the specifics of the codebase
    pattern = re.compile(r'function\s+(\w+)\s*\((.*?)\)\s*\{([\s\S]*?)\}', re.MULTILINE)
    return pattern.findall(diff)

def get_full_function_at_commit(repo, commit_hash, function_name, file_path):
    # Get the commit object
    commit = repo.commit(commit_hash)

    # Find the file in the commit tree
    for blob in commit.tree.traverse():
        if blob.path == file_path:
            # Read the file content
            file_content = blob.data_stream.read().decode('utf-8')

            # Regular expression to match the specific function
            pattern = re.compile(r'function\s+' + re.escape(function_name) + r'\s*\((.*?)\)\s*\{([\s\S]*?)\}', re.MULTILINE)
            match = pattern.search(file_content)

            if match:
                return {'args': match.group(1), 'body': match.group(2)}

    print(f"Function '{function_name}' not found in commit '{commit_hash}'")
    return None


functions = {}

for commit in merge_commits:
    parent_commit = commit.parents[0]
    diffs = commit.diff(parent_commit, create_patch=True)

    print(f"Commit: {commit.hexsha}")
    for diff in diffs:
        print(f"File: {diff.a_path} (Change Type: {diff.change_type})")
        diff_content = diff.diff.decode('utf-8')
        for func_name, _, _ in extract_js_functions(diff_content):
            if func_name not in functions:
                full_function = get_full_function_at_commit(repo, commit.hexsha, func_name, diff.a_path)
                if full_function:
                    functions[func_name] = {'args': full_function['args'], 'body': full_function['body'], 'commit': commit.hexsha}
                    print(f"Function '{func_name}' captured from merge commit.")

    print("\n")

# Save the functions into a file called 'function_changes.json' in ./outputData
with open('./outputData/function_changes.json', 'w') as fp:
    json.dump(functions, fp, indent=4)

