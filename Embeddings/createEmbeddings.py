import openai
import requests
import json
import os
import dotenv

# Set the OpenAI API key using the environment variable
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the input text for which you want to get the embedding
input_text = "function testingTheChange() {\n+  console.log('This the original function');\n+}"

# Specify the embedding model
model = "text-embedding-ada-002"

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
print(embedding)
