import openai
import requests
import json
import os
import dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

def process_user_input(input_function):
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def embedUserInput():
        # Use the input function directly
        model = "text-embedding-ada-002"
        input_text = input_function

        data = {
            "input": input_text,
            "model": model
        }
        # standard OpenAI call
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

    def performKNNSearch(embedding, k=5, merge_threshold=-0.6):
        # Initialize the Qdrant client
        client = QdrantClient(host='localhost', port=6333)

        # Perform the k-NN search
        search_results = client.search(
            collection_name="functions",
            query_vector=embedding,
            search_params=models.SearchParams(hnsw_ef=128, exact=False),
            limit=k
        )

        # Process the search results
        if 'result' in search_results:
            results = search_results['result']
        else:
            results = search_results

        total_score = 0
        for result in results:
            payload = result.payload
            score = payload['score'] if 'score' in payload else 0
            total_score += score
        average_score = total_score / k 
        
        should_merge = "🎉 Merge the function 🎉" if average_score <= merge_threshold else "🙅 Do not merge the function 🙅"

        return should_merge

    embed = embedUserInput()
    return performKNNSearch(embed)
    
if __name__ == '__main__':
    function_input = "async function buildBlogFeed(ul, pageNum, pageControl) {\n  const limit = 10;\n  const offset = pageNum * limit;\n  let morePages = false;\n  const blogPosts = ffetch('/query-index.json')\n    .filter((p) => p.path.startsWith('/blog/'))\n    .slice(offset, offset + limit + 1);\n\n  let i = 0;\n  const newUl = document.createElement('ul');\n  // eslint-disable-next-line no-restricted-syntax\n  for await (const post of blogPosts) {\n    if (i >= limit) {\n      // skip render, but know we have more page\n      morePages = true;\n      break;\n    }\n\n    const li = document.createElement('li');\n    li.append(buildPost(post, i < 1));\n    newUl.append(li);\n\n    i += 1;\n  }\n\n  pageControl.innerHTML = `\n      <ul class=\"pages\">\n        <li class=\"prev\"><a data-page=\"${pageNum - 1}\" href=\"${window.location.pathname}?page=${pageNum}\"><span class=\"icon icon-next\"><span class=\"sr-only\">Previous Page</span></a></li>\n        <li class=\"cur\"><span>${pageNum + 1}</span></li>\n        <li class=\"next\"><a data-page=\"${pageNum + 1}\" href=\"${window.location.pathname}?page=${pageNum + 2}\"><span class=\"icon icon-next\"></span><span class=\"sr-only\">Next Page</span></a></li>\n      </ul>\n    `;\n\n  if (pageNum === 0) {\n    pageControl.querySelector('.prev').remove();\n  }\n\n  if (!morePages) {\n    pageControl.querySelector('.next').remove();\n  }\n\n  pageControl.querySelectorAll('li > a').forEach((link) => {\n    link.addEventListener('click', (evt) => {\n      evt.preventDefault();\n      buildBlogFeed(ul, Number(link.dataset.page), pageControl);\n    });\n  });\n\n  decorateIcons(pageControl);\n  ul.innerHTML = newUl.innerHTML;\n  window.scrollTo({\n    top: 0,\n    behavior: 'smooth',\n  });\n}"
    print(process_user_input(function_input))
    
