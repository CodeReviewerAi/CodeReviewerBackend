import json
import numpy as np
from collections import Counter

def log_normalize_change_counts(repos):
    # Apply logarithmic normalization
    all_changes = [func['changes_after_merge'] + 1 for repo in repos.values() for func in repo.values()]
    log_changes = np.log(all_changes)
    min_log, max_log = min(log_changes), max(log_changes)

    for repo_name, functions in repos.items():
        for func_key, func_info in functions.items():
            adjusted_change = np.log(func_info['changes_after_merge'] + 1)
            normalized_score = 2 * ((adjusted_change - min_log) / (max_log - min_log)) - 1
            func_info['score'] = normalized_score
    return repos

def analyze_changes_distribution(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    normalized_data = log_normalize_change_counts(data)

    # Original changes
    original_changes = [func['changes_after_merge'] for repo in data.values() for func in repo.values()]
    # Normalized scores
    normalized_scores = [func['score'] for repo in normalized_data.values() for func in repo.values()]

    # Statistics for original changes
    min_changes, max_changes = min(original_changes), max(original_changes)
    mean_changes, median_changes = np.mean(original_changes), np.median(original_changes)
    changes_counter = Counter(original_changes)

    # Statistics for normalized scores
    min_score, max_score = min(normalized_scores), max(normalized_scores)
    mean_score, median_score = np.mean(normalized_scores), np.median(normalized_scores)
    score_counter = Counter(normalized_scores)

    # Print statistics
    print(f"File: {file_path}")
    print("Original 'changes_after_merge' statistics:")
    print(f"  Min: {min_changes}, Max: {max_changes}, Mean: {mean_changes:.2f}, Median: {median_changes}")
    print("  Distribution of changes:")
    for change, freq in changes_counter.items():
        print(f"    Changes: {change}, Frequency: {freq}")

    print("\nNormalized score statistics:")
    print(f"  Min: {min_score:.2f}, Max: {max_score:.2f}, Mean: {mean_score:.2f}, Median: {median_score:.2f}")
    print("  Distribution of scores:")
    for score, freq in score_counter.items():
        print(f"    Score: {score:.2f}, Frequency: {freq}")

if __name__ == '__main__':
    analyze_changes_distribution('../dataForTesting/training.json')
    analyze_changes_distribution('../dataForTesting/testing.json')
