import openai
import requests
import json
import os
import dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def embedUserInput():
    Json_path = './inputFunction.json'
    with open(Json_path, 'r') as file:
        json_data = json.load(file)

    model = "text-embedding-ada-002"
    input_text = json_data['function']

    data = {
        "input": input_text,
        "model": model
    }

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

def performKNNSearch(embedding, k=5):
    # Initialize the Qdrant client
    client = QdrantClient(host='localhost', port=6333)

    # Perform the k-NN search
    search_results = client.search(
        collection_name="functions",
        query_vector=embedding,
        search_params=models.SearchParams(hnsw_ef=128, exact=False), # No idea what this does
        limit=k
    )


   # Check if 'result' is a valid key in the search results
    if 'result' in search_results:
        results = search_results['result']
    else:
        # If 'result' is not a key, assume search_results is a list of results
        results = search_results

    # Extract the payloads and compute the average
    total_score = 0
    for result in results:
        # Access the payload and score using the appropriate method or property
        payload = result.payload
        score = payload['score'] if 'score' in payload else 0
        total_score += score

    average_score = total_score / k if k > 0 else 0

    return average_score

embed = embedUserInput()
print(performKNNSearch(embed))