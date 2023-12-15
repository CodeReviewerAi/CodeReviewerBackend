import git
import json
import re
from datetime import datetime

# Path to your repository
repo_path = 'inputData/testRepo2'
repo = git.Repo(repo_path)

merge_commits = [commit for commit in repo.iter_commits('main') if commit.parents and len(commit.parents) > 1]
merge_commits.reverse()  # Reverse the list to get the oldest merge commit first

def get_func_name(diff):
    pattern = re.compile(r'function\s+(\w+)\s*\((.*?)\)\s*\{([\s\S]*?)\}', re.MULTILINE)
    return pattern.findall(diff)

def get_full_function_at_commit(repo, commit_hash, function_name, file_path): 
    commit = repo.commit(commit_hash)
    blob = commit.tree / file_path
    file_content = blob.data_stream.read().decode('utf-8')

    pattern = re.compile(r'function\s+' + re.escape(function_name) + r'\s*\((.*?)\)\s*\{([\s\S]*?)\}', re.MULTILINE)
    match = pattern.search(file_content)

    if match:
        full_function = f"function {function_name}({match.group(1)}) {{{match.group(2)}}}"
        return full_function

    return None

functions = {}

for commit in merge_commits:
    parent_commit = commit.parents[0]
    diffs = commit.diff(parent_commit, create_patch=True)

    for diff in diffs:
        diff_content = diff.diff.decode('utf-8')
        for func_name, _, _ in get_func_name(diff_content):
            full_function = get_full_function_at_commit(repo, commit.hexsha, func_name, diff.a_path)
            if full_function:
                if func_name not in functions:
                    functions[func_name] = {
                        'merged_function': full_function,
                        'commit': commit.hexsha,
                        'changes_after_merge': 0,
                        'latest_function': full_function,
                        'time_first_merged': commit.authored_datetime,
                        'file_path': diff.a_path  # Store file path here
                    }

for func_name, func_info in functions.items():
    for commit in repo.iter_commits('main', reverse=True):  # Iterate from the oldest to newest
        if commit.authored_datetime > func_info['time_first_merged']:
            try:
                blob = commit.tree / func_info['file_path']
                file_content = blob.data_stream.read().decode('utf-8')
                new_content = get_full_function_at_commit(repo, commit.hexsha, func_name, func_info['file_path'])
                if new_content and new_content.strip() != func_info['latest_function'].strip():
                    func_info['changes_after_merge'] += 1
                    func_info['latest_function'] = new_content
                    print(f"Function '{func_name}' changed at commit {commit.hexsha}")
            except KeyError:
                continue

# Convert datetime objects to string before saving
for func in functions.values():
    func['time_first_merged'] = func['time_first_merged'].isoformat()

# Save the functions and their change counts into a file
with open('functionRetriever/outputData/function_changes.json', 'w') as fp:
    json.dump(functions, fp, indent=4)