import openai
import requests
import json
import os
import time
import dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

def process_user_input(input_function):
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def embedUserInput(retry_attempts=3, retry_delay=5):
        model = "text-embedding-ada-002"
        input_text = input_function
        data = {"input": input_text, "model": model}
        
        for attempt in range(retry_attempts):
            try:
                response = requests.post(
                    'https://api.openai.com/v1/embeddings',
                    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {openai.api_key}'},
                    data=json.dumps(data)
                )
                if response.status_code == 200:
                    return response.json()['data'][0]['embedding']
                else:
                    print(f"Failed to get embedding, status code: {response.status_code}. Retrying...")
            except Exception as e:
                print(f"Exception during embedding request: {e}. Retrying...")
            
            time.sleep(retry_delay)

        raise Exception("Failed to embed input after multiple attempts.")

    def performKNNSearch(embedding, k=5, merge_threshold=-0.6):
        client = QdrantClient(host='localhost', port=6333)

        search_results = client.search(
            collection_name="functions",
            query_vector=embedding,
            search_params=models.SearchParams(hnsw_ef=128, exact=False),
            limit=k
        )

        if 'result' in search_results:
            results = search_results['result']
        else:
            results = search_results

        total_score = sum(result.payload.get('score', 0) for result in results)
        average_score = total_score / k
        return "🎉 Merge the function 🎉" if average_score <= merge_threshold else "🙅 Do not merge the function 🙅"

    embedding = embedUserInput()
    return performKNNSearch(embedding)
    
if __name__ == '__main__':
    function_input = "async function buildBlogFeed(ul, pageNum, pageControl) {...}"  # truncated for brevity
    print(process_user_input(function_input))
