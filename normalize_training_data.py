import json

def normalize_change_counts(repos):
    for repo_name, functions in repos.items():
        # Extract changes_after_merge values and find min and max
        changes = [func['changes_after_merge'] for func in functions.values()]
        min_changes, max_changes = min(changes), max(changes)

        # Normalize the change counts between -1 and 1 for each function
        for func_key, func_info in functions.items():
            if max_changes != 0:  # Check to avoid division by zero
                normalized_score = 2 * (func_info['changes_after_merge'] / max_changes) - 1
            else:
                normalized_score = -1  # Assign -1 if all changes are 0
            func_info['score'] = normalized_score

    return repos

# Load your data
with open('./dataForTesting/training.json', 'r') as f:
    data = json.load(f)

# Normalize data
normalized_data = normalize_change_counts(data)

# Save the normalized data back to the JSON file
with open('./dataForTesting/training.json', 'w') as f:
    json.dump(normalized_data, f, indent=4)
