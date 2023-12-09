import openai
import requests
import json
import os
import random
import dotenv
from qdrant_client import models, QdrantClient

# Initialize Qdrant Client
qdrant_client = QdrantClient(host='localhost', port=6333)  # Adjust host and port as necessary

# Set the OpenAI API key using the environment variable
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the JSON data from the file
json_file_path = '../outputData/function_changes.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Specify the embedding model
model = "text-embedding-ada-002"

# Initialize the Qdrant client
dimension_vector = 1536
qdrant = QdrantClient(":memory:")
qdrant.recreate_collection(
    collection_name="functions",
    vectors_config=models.VectorParams(
        size=dimension_vector,
        distance=models.Distance.COSINE,
    ),
)

# Process each function in the JSON data
for function_name, function_data in list(json_data.items())[:5]: # Limit to 5 functions for testing should be #for function_name, function_data in json_data.items():
    input_text = function_data['first_version']

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
        "score": function_data['count'],
    }

    # Add the embedding to Qdrant
    qdrant.upload_records(
        collection_name="functions",
        records=[
            models.Record(
                id=id, 
                vector=embedding,
                payload=payload
            )
        ]
    )
    print(f"Added function '{function_name}' to Qdrant with ID {id}")
