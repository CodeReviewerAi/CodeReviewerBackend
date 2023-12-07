import subprocess

def getAllCommitsWhereJSFilesWhereChanged(repo_path):
    command = ["git", "-C", repo_path, "log", "--pretty=format:%H %s", "--", "*.js"]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')

def main():
    repo_path = './inputData/walgreens'
    commits = getAllCommitsWhereJSFilesWhereChanged(repo_path)
    for commit in commits:
        print(commit)
    print('Total commits:', len(commits))

if __name__ == "__main__":
    main()
