import os
import git
import json
import time
import subprocess

def get_function_data(repo_path='../inputData/testRepo'):
    output_file = 'outputData/test_function_changes.json' if repo_path.endswith('testRepo') else 'outputData/function_changes.json'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(script_dir, repo_path)
    repo = git.Repo(repo_path)

    repo.git.checkout('main')
    repo.git.pull()

    merge_commits = [commit for commit in repo.iter_commits('main') if commit.parents and len(commit.parents) > 1]
    merge_commits.reverse()

    ast_cache = {}

    def get_ast_from_js(file_content):
        # Generate a hash of the file content
        content_hash = hash(file_content)

        # Check if the AST is already in the cache
        if content_hash in ast_cache:
            return ast_cache[content_hash]

        process = subprocess.Popen(['node', 'babelParser.js'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=file_content)
        if stderr:
            print("Error in parsing:", stderr)
            return None

        # Parse the output and store the AST in the cache
        ast = json.loads(stdout)
        ast_cache[content_hash] = ast
        return ast

    def get_functions_from_file(file_content):
        # create ast from file content
        ast = get_ast_from_js(file_content)

        functions = []
        try:
            # Traverse the AST to find function declarations
            def traverse(node):
                if not isinstance(node, dict):
                    return

                if 'type' in node:
                    # Check for arrow functions or function expressions assigned to variables
                    if node['type'] in ['VariableDeclarator'] and 'init' in node:
                        init_node = node['init']
                        if init_node and 'type' in init_node and init_node['type'] in ['FunctionExpression', 'ArrowFunctionExpression']:
                            function_name = None
                            if 'name' in node['id']:
                                function_name = node['id']['name']
                            if function_name:
                                functions.append(function_name)

                    # Existing checks for FunctionDeclaration, etc.
                    elif node['type'] in ['FunctionDeclaration', 'FunctionExpression', 'ArrowFunctionExpression']:
                        function_name = None
                        if 'id' in node and node['id'] is not None:
                            function_name = node['id']['name']
                        elif 'key' in node and 'name' in node['key']:
                            function_name = node['key']['name']
                        if function_name:
                            functions.append(function_name)

                    # Check for methods in classes
                    if node['type'] == 'MethodDefinition' and 'key' in node and node['key']['type'] == 'Identifier':
                        functions.append(node['key']['name'])

                # Recursively traverse child nodes
                for key, value in node.items():
                    if isinstance(value, dict):
                        traverse(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                traverse(item)

            traverse(ast['program'])
        except Exception as e:
            print(f"Error processing AST: {e}")
        return functions
    
    def normalize_change_counts(functions):
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

        return functions


    def get_full_function_at_commit(repo, commit_hash, function_name, file_path):
        commit = repo.commit(commit_hash)
        blob = commit.tree / file_path
        file_content = blob.data_stream.read().decode('utf-8')

        # create ast from file content
        ast = get_ast_from_js(file_content)

        try:
            # Define a function to recursively search for the function
            def find_function(node, function_name):
                if not isinstance(node, dict):
                    return None

                # Handle different types of function nodes
                if node.get('type') == 'FunctionDeclaration' and node.get('id', {}).get('name') == function_name:
                    return node.get('start'), node.get('end')

                if node.get('type') == 'VariableDeclarator':
                    init_node = node.get('init')
                    if isinstance(init_node, dict) and init_node.get('type') in ['FunctionExpression', 'ArrowFunctionExpression']:
                        if node.get('id', {}).get('name') == function_name:
                            return node.get('start'), node.get('end')

                # Recursive traversal
                for key, value in node.items():
                    if isinstance(value, dict):
                        result = find_function(value, function_name)
                        if result:
                            return result
                    elif isinstance(value, list):
                        for item in value:
                            result = find_function(item, function_name)
                            if result:
                                return result
                return None

            # Search for the function in the AST
            start_end = find_function(ast['program'], function_name)  # Pass function_name here
            if start_end:
                start, end = start_end
                return file_content[start:end]
        except Exception as e:
            print(f"Error processing AST: {e}")

        return None

    functions = {}




    for commit in merge_commits:
        print(f"Processing merge commit {commit.hexsha}")
        for file_path in commit.stats.files:
            if file_path.endswith('.js'):
                try:
                    blob = commit.tree / file_path
                    file_content = blob.data_stream.read().decode('utf-8')
                    for func_name in get_functions_from_file(file_content):
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
                except Exception as e:
                        print(f"Error processing commit {commit.hexsha}: {e}")
                        continue

    for commit in repo.iter_commits('main', reverse=True):  # Iterate from the oldest to newest commit
        print(f"Processing commit {commit.hexsha}")
        for file_path in commit.stats.files:
            if file_path.endswith('.js'):
                try:
                    blob = commit.tree / file_path
                    file_content = blob.data_stream.read().decode('utf-8')
                    current_functions = get_functions_from_file(file_content)

                    for func_key, func_info in functions.items():
                        if func_info['file_path'] == file_path:
                            if func_info['function_name'] in current_functions:
                                new_content = get_full_function_at_commit(repo, commit.hexsha, func_info['function_name'], file_path)
                                if new_content and new_content.strip() != func_info['latest_function'].strip() and commit.authored_datetime > func_info['time_first_merged']:
                                    func_info['changes_after_merge'] += 1
                                    func_info['latest_function'] = new_content
                except Exception as e:
                    print(f"Error processing commit {commit.hexsha}: {e}")
                    continue

    # Normalize the change counts to a score between -1 and 1
    # functions = normalize_change_counts(functions)

    # Convert datetime objects to string before saving
    for func in functions.values():
        func['time_first_merged'] = func['time_first_merged'].isoformat()

    # Save only specific keys in the JSON file
    filtered_functions = {}
    for func_key, func_info in functions.items():
        filtered_functions[func_key] = {
            'changes_after_merge': func_info['changes_after_merge'],
            'file_path': func_info['file_path'],
            'merged_function': func_info['merged_function'],
        }

    # Save the filtered data into a file
    with open(output_file, 'w') as f:
        json.dump(filtered_functions, f, indent=4)

if __name__ == '__main__':
    start_time = time.time()
    get_function_data(repo_path='../inputData/trainingData/danaher-ls-aem') #pass this variable if you want to run another repo than testRepo: repo_path='../inputData/elixirsolutions'
    end_time = time.time()
    elapsed_time = round((end_time - start_time) / 60, 2)  # convert to minutes and round to 2 decimal places
    print('✅ Printed function data to outputData/test_function_changes.json ✅')
    print(f'⏰ The program took {elapsed_time} minutes to run. ⏰')