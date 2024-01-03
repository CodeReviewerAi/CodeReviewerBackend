import openai
import requests
import json
import os
import random
import dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionDescription, Distance, VectorParams, Record

def embed_sample_functions(repo_path):
    # Initialize Qdrant Client
    client = QdrantClient(host='localhost', port=6333)
    # client = QdrantClient(":memory:")

    # Set the OpenAI API key using the environment variable
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Load the JSON data from the file
    json_file_path = 'outputData/test_function_changes.json' if repo_path.endswith('testRepo') else 'outputData/function_changes.json'
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)

    # Specify the embedding model
    model = "text-embedding-ada-002"

    if client.get_collections().collections.__contains__(CollectionDescription(name='functions')):
        client.recreate_collection(
            collection_name="functions",
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )
    else:
        client.create_collection(
            collection_name="functions",
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )

    # Process each function in the JSON data
    for function_name, function_data in list(json_data.items())[:5]: # Limit to 5 functions for testing should be #for function_name, function_data in json_data.items():
        input_text = function_data['merged_function']

        # Create the data for the POST request
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

        #create the random id
        id = random.randint(0,1000000)

        # create the payload
        payload = {
            "function_name": function_name,
            "score": function_data['score'],
        }

        # Add the embedding to Qdrant
        client.upload_records(
            collection_name="functions",
            records=[
                Record(
                    id=id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )
        print(f"Added function '{function_name}' to Qdrant with ID {id}")
