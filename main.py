import subprocess
import re
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

    for commit in commits:
        diff = get_commit_diff(repo_path, commit)
        functions = extract_functions(diff)

        for function_name in functions:
            full_function = 'function ' + function_name + diff.split(function_name)[1].split('}')[0] + '}'

            function_hash = hash_function_body(full_function)

            if function_name not in function_changes:
                function_changes[function_name] = {'count': 0, 'hashes': set()}
            
            if function_hash not in function_changes[function_name]['hashes']:
                function_changes[function_name]['count'] += 1
                function_changes[function_name]['hashes'].add(function_hash)

    return function_changes

def main():
    repo_path = './inputData/walgreens'
    commits = get_js_commits(repo_path)
    function_changes = analyze_commits(repo_path, commits)

    for function_name, data in function_changes.items():
        print(f"Function '{function_name}' changed {data['count']} times")

if __name__ == "__main__":
    main()
