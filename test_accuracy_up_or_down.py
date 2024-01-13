import subprocess
import re

# ANSI escape codes for colors
GREEN = '\033[92m'  # Green text
RED = '\033[91m'    # Red text
ENDC = '\033[0m'    # Reset color

def get_last_commit_on_main():
    return subprocess.check_output(['git', 'rev-parse', 'main']).decode().strip()

def get_diff_of_readme(last_commit):
    return subprocess.check_output(['git', 'diff', last_commit, 'README.md']).decode()

def parse_accuracy_from_diff(diff):
    pattern = r"## Current Accuracy: (\d+\.\d+)%"
    accuracies = re.findall(pattern, diff)
    return [float(acc) for acc in accuracies]

def test_accuracy_increase():
    try:
        last_commit = get_last_commit_on_main()
        diff = get_diff_of_readme(last_commit)
        if '## Current Accuracy:' in diff:
            old_accuracy, new_accuracy = parse_accuracy_from_diff(diff)
            assert new_accuracy > old_accuracy, "Accuracy must be increased in PR"
            return True
        else:
            print("No accuracy update in README.md 🤷‍♂️")
            return False
    except Exception as e:
        print(f"Test failed due to an error: {e} ❌")
        return False

if __name__ == '__main__':
    result = test_accuracy_increase()
    if result:
        print(GREEN + "Test passed: Accuracy has been increased! 🎉" + ENDC)
    else:
        print(RED + "Test failed: Accuracy has not been increased or no accuracy update was found. 😢" + ENDC)
