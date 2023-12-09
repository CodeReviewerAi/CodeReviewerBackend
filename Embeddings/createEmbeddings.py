import openai
import requests
import json
import os
import dotenv

# Set the OpenAI API key using the environment variable
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the JSON data from the file
json_file_path = '../outputData/function_changes.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Specify the embedding model
model = "text-embedding-ada-002"

# Process each function in the JSON data
for function_name, function_data in json_data.items():
    input_text = function_data['first_version']

    # Create the data for the POST request
    data = {
        "input": input_text,
        "model": model
    }

    # Make the API request
    response = requests.post(
        'https://api.openai.com/v1/embeddings',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai.api_key}'
        },
        data=json.dumps(data)
    )

    # Extract and print the embedding from the response
    embedding = response.json()['data'][0]['embedding']
    print(f"Embedding for {function_name}:", embedding)
