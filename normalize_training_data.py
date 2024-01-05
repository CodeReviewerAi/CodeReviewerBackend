import json
import numpy as np

def log_normalize_change_counts(repos):
    # Extract all changes and adjust by adding 1
    all_changes = [func['changes_after_merge'] + 1 for repo in repos.values() for func in repo.values()]
    
    # Apply logarithmic transformation
    log_changes = np.log(all_changes)
    min_log, max_log = min(log_changes), max(log_changes)

    # Normalize each repository's changes
    for repo_name, functions in repos.items():
        for func_key, func_info in functions.items():
            adjusted_change = np.log(func_info['changes_after_merge'] + 1)
            normalized_score = 2 * ((adjusted_change - min_log) / (max_log - min_log)) - 1
            func_info['score'] = normalized_score

    return repos

def normalize_and_save_change_counts(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    normalized_data = log_normalize_change_counts(data)

    with open(file_path, 'w') as f:
        json.dump(normalized_data, f, indent=4)

    return normalized_data

if __name__ == '__main__':
    normalize_and_save_change_counts('dataForTesting/training.json')
    normalize_and_save_change_counts('dataForTesting/testing.json')
