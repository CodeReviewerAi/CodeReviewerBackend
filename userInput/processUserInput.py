import openai
import requests
import json
import os
import random
import dotenv

def embedUserInput():
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    Json_path = './inputFunction.json'
    with open(Json_path, 'r') as file:
        json_data = json.load(file)

    model = "text-embedding-ada-002"
    input_text = json_data['function']

    data = {
        "input": input_text,
        "model": model
    }

    # Make the API request for embeddings
    response = requests.post(
        'https://api.openai.com/v1/embeddings',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai.api_key}'
        },
        data=json.dumps(data)
    )
    embedding = response.json()['data'][0]['embedding']
    return embedding

print(embedUserInput())