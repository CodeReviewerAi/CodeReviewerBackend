import git
import json
import re

# Path to your repository
repo_path = '../inputData/testRepo2'
repo = git.Repo(repo_path)

merge_commits = [commit for commit in repo.iter_commits('main') if commit.parents and len(commit.parents) > 1]
merge_commits.reverse() # Reverse the list to get the oldest merge commit first 

def extract_js_functions(diff):
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
        for func_name, _, _ in extract_js_functions(diff_content):
            full_function = get_full_function_at_commit(repo, commit.hexsha, func_name, diff.a_path)
            if full_function:
                if func_name not in functions:
                    functions[func_name] = {
                        'function': full_function,
                        'commit': commit.hexsha,
                        'change_count': 0,
                        'latest_content': full_function
                    }
                elif functions[func_name]['latest_content'] != full_function:
                    functions[func_name]['change_count'] += 1
                    functions[func_name]['latest_content'] = full_function
                    print(f"Function {func_name} changed at commit {commit.hexsha}")

# Save the functions and their change counts into a file
with open('./outputData/function_changes.json', 'w') as fp:
    json.dump(functions, fp, indent=4)

# Current issues
# - Functions with the same name are treated as the same function
# - Functions that are renamed are treated as different functions
# - Does not keep track of changes that are not merge commits (When a function was changed on main or multiple commits were merged into main)