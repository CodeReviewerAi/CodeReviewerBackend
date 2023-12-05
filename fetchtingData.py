# This is the old approach, using the GitHub API to fetch the file content.

import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_js_files(base_url, path='', headers=None):
    if headers is None:
        headers = {} # Empty headers by default

    js_files = []
    full_url = f"{base_url}/{path}" if path else base_url

    response = requests.get(full_url, headers=headers) # Fetch directory listing
    if response.status_code == 200:
        items = response.json()
        for item in items:
            if item['type'] == 'file' and item['name'].endswith('.js'):
                js_files.append(item['path'])
            elif item['type'] == 'dir':
                subdir_path = item['path']
                js_files.extend(get_js_files(base_url, subdir_path, headers))
    else:
        print('Failed to get directory listing, Status Code:', response.status_code)
    return js_files

def fetch_file_content(url, headers):
    # Fetches file content from GitHub
    response = requests.get(url, headers=headers) # Fetch file content
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f'Failed to fetch file: {response.status_code}')

def extract_function_names(file_content):
    # Extracts function names from file content
    pattern = r'function (\w+)\s*\('
    return re.findall(pattern, file_content)

def main():
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}

    base_url = 'https://api.github.com/repos/hlxsites/bitdefender/contents'
    start_path = 'solutions'

    try:
        js_files = get_js_files(base_url, start_path, headers)
        for js_file in js_files:
            file_url = f'https://raw.githubusercontent.com/hlxsites/bitdefender/main/{js_file}'
            file_content = fetch_file_content(file_url, headers)
            function_names = extract_function_names(file_content)
            print(f"Functions in {js_file}: {function_names}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
