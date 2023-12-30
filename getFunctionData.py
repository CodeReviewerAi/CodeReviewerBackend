import re
import os
import git
import json
import subprocess

def get_function_data(repo_path='../inputData/testRepo2'):
    output_file = 'outputData/test_function_changes.json' if repo_path.endswith('testRepo2') else 'outputData/function_changes.json'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(script_dir, repo_path)
    repo = git.Repo(repo_path)

    repo.git.checkout('main')
    repo.git.pull()

    merge_commits = [commit for commit in repo.iter_commits('main') if commit.parents and len(commit.parents) > 1]
    merge_commits.reverse()

    def get_ast_from_js(file_content, temp_file_path):
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(file_content)
        result = subprocess.run(['node', 'babelParser.js', temp_file_path], capture_output=True, text=True)
        if result.stderr:
            print("Error in parsing:", result.stderr)
            return None
        return json.loads(result.stdout)

    def get_functions_from_file(file_content):
        temp_file_path = 'temp.js'  # Temporary file to store the content
        ast = get_ast_from_js(file_content, temp_file_path)
        if not ast: 
            return []

        functions = []
        try:
            # Access the 'body' within 'program' of the AST
            for node in ast['program']['body']:
                if node['type'] == 'FunctionDeclaration':
                    function_name = node['id']['name'] if node.get('id') else None
                    if function_name:
                        functions.append(function_name)
        except Exception as e:
            print(f"Error processing AST: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)  # Clean up the temporary file
        return functions

    def get_full_function_at_commit(repo, commit_hash, function_name, file_path):
        commit = repo.commit(commit_hash)
        blob = commit.tree / file_path
        file_content = blob.data_stream.read().decode('utf-8')

        temp_file_path = 'temp.js'
        ast = get_ast_from_js(file_content, temp_file_path)
        if not ast:
            return None

        try:
            # Access the 'body' within 'program' of the AST
            for node in ast['program']['body']:
                if node['type'] == 'FunctionDeclaration' and node.get('id', {}).get('name') == function_name:
                    start, end = node['start'], node['end']
                    return file_content[start:end]
        except Exception as e:
            print(f"Error processing AST: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)  # Clean up the temporary file
        return None

    functions = {}

    for commit in merge_commits:
        for file_path in commit.stats.files:
            if file_path.endswith('.js'):
                commit = repo.commit(commit.hexsha)
                print(f"Processing commit {commit.hexsha}...")
                blob = commit.tree / file_path
                file_content = blob.data_stream.read().decode('utf-8')
                print(f"File path: {file_path}")
                for func_name in get_functions_from_file(file_content):
                    full_function = get_full_function_at_commit(repo, commit.hexsha, func_name, file_path)
                    print(f"Processing function: {func_name}")
                    if full_function:
                        func_key = f"{file_path}::{func_name}"
                        if func_key not in functions:
                            print(f"New function found: {func_key}")
                            functions[func_key] = {
                                'function_name': func_name,
                                'merged_function': full_function,
                                'commit': commit.hexsha,
                                'changes_after_merge': 0,
                                'latest_function': full_function,
                                'time_first_merged': commit.authored_datetime,
                                'file_path': file_path
                            }
                print(f"Finished processing commit {commit.hexsha}\n")

    for func_key, func_info in functions.items():
        for commit in repo.iter_commits('main', reverse=True):  # Iterate from the oldest to newest
            print(f"Processing commit in the second loop{commit.hexsha}...")
            # print the number of the commit where 1 is the oldest commit
            print(f"Commit number: {commit.count()}")
            if commit.authored_datetime > func_info['time_first_merged']:
                try:
                    blob = commit.tree / func_info['file_path']
                    file_content = blob.data_stream.read().decode('utf-8')
                    new_content = get_full_function_at_commit(repo, commit.hexsha, func_info['function_name'], func_info['file_path'])
                    if new_content and new_content.strip() != func_info['latest_function'].strip():
                        print(f"Found change in function {func_key} at commit {commit.hexsha}")
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
    #get_function_data(repo_path='../inputData/elixirsolutions')
    get_function_data()
    print('Printed function data to outputData/test_function_changes.json ✅')

    # Todo:
    # - Fix tests the issue is that they are not valid JS
    # - reduce runtime by optimizing 