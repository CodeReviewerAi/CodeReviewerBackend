import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_js_files(base_url, path='', token=''):
    js_files = []
    headers = {'Authorization': f'token {token}'} if token else {}
    full_url = f"{base_url}/{path}" if path else base_url

    response = requests.get(full_url, headers=headers)
    if response.status_code == 200:
        items = response.json()
        for item in items:
            if item['type'] == 'file' and item['name'].endswith('.js'):
                js_files.append(item['path'])
            elif item['type'] == 'dir':
                subdir_path = item['path']
                js_files.extend(get_js_files(base_url, subdir_path, token))
    else:
        print('Failed to get directory listing, Status Code:', response.status_code)
    return js_files

token = os.getenv('GITHUB_TOKEN')

# Base URL for GitHub API
base_url = 'https://api.github.com/repos/hlxsites/bitdefender/contents'
# Starting path from the repository root
start_path = 'solutions'

js_files = get_js_files(base_url, start_path, token=token)
for js_file in js_files:
    print(js_file)

