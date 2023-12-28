import git
import json
import re
import os

def get_function_data(repo_path='../inputData/testRepo2'):
    output_file = 'outputData/test_function_changes.json' if repo_path.endswith('testRepo2') else 'outputData/function_changes.json'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(script_dir, repo_path)
    repo = git.Repo(repo_path) 
    
    repo.git.checkout('main')
    repo.git.pull()

    merge_commits = [commit for commit in repo.iter_commits('main') if commit.parents and len(commit.parents) > 1]
    merge_commits.reverse()

    def get_functions_from_file(file_content):
        pattern = re.compile(r'function\s+([^\(]+)\s*\(([^)]*)\)\s*{', re.MULTILINE)
        return pattern.findall(file_content)

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
        for file_path in commit.stats.files:
            if file_path.endswith('.js'):  # Only consider JavaScript files
                commit = repo.commit(commit.hexsha)
                blob = commit.tree / file_path
                file_content = blob.data_stream.read().decode('utf-8')
                for func_name, _ in get_functions_from_file(file_content):
                    full_function = get_full_function_at_commit(repo, commit.hexsha, func_name, file_path)
                    if full_function:
                        func_key = f"{file_path}::{func_name}"
                        if func_key not in functions:
                            functions[func_key] = {
                                'function_name': func_name,
                                'merged_function': full_function,
                                'commit': commit.hexsha,
                                'changes_after_merge': 0,
                                'latest_function': full_function,
                                'time_first_merged': commit.authored_datetime,
                                'file_path': file_path
                            }


    for func_key, func_info in functions.items():
        for commit in repo.iter_commits('main', reverse=True):  # Iterate from the oldest to newest
            if commit.authored_datetime > func_info['time_first_merged']:
                try:
                    blob = commit.tree / func_info['file_path']
                    file_content = blob.data_stream.read().decode('utf-8')
                    new_content = get_full_function_at_commit(repo, commit.hexsha, func_info['function_name'], func_info['file_path'])
                    if new_content and new_content.strip() != func_info['latest_function'].strip():
                        func_info['changes_after_merge'] += 1
                        func_info['latest_function'] = new_content
                except KeyError:
                    continue

    # Find the min and max changes after merge
    min_changes = min(functions.values(), key=lambda x: x['changes_after_merge'])['changes_after_merge']
    max_changes = max(functions.values(), key=lambda x: x['changes_after_merge'])['changes_after_merge']

    # Normalize the change counts between -1 and 1
    for func_key, func_info in functions.items():
        if max_changes != min_changes:
            normalized_score = 2 * ((func_info['changes_after_merge'] - min_changes) / (max_changes - min_changes)) - 1
        else:
            normalized_score = 0
        func_info['score'] = normalized_score

    # Convert datetime objects to string before saving
    for func in functions.values():
        func['time_first_merged'] = func['time_first_merged'].isoformat()

    # Save the functions and their change counts and normalized scores into a file
    with open(output_file, 'w') as f:
        json.dump(functions, f, indent=4)

if __name__ == '__main__':
    # pass repo_path variable if you want to test on another repo other than default
    #repo_path='../inputData/elixirsolutions'
    get_function_data()
    print('Printed function data to outputData/test_function_changes.json ✅')