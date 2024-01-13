# What is CodeReviewer?
CodeReviewer is a tool that uses machine learning to help developers reviewing code. It is trained on a dataset of code from the [hlxsites](https://github.com/hlxsites) repositories and is able to predict how likely a given function is going to break in the future.

## Current Accuracy: 73.28%

## How does it work?
We save each functions first version(When it was first merged) and how often it was changed in the future. We then use this data to create embeddings for each function. We then use these embeddings to create a database using Qdrant. 
When a user uploads a function, we use the embeddings to find the 5 most similar functions in the database. We then use the number of times these functions were changed to predict how likely the user's function is to break in the future.

---

# Quickstart Guide
## Installation
- run `pip install -r requirements.txt` to install all dependencies all Python dependencies
- run `npm install` to install all Node dependencies
- Install [Docker](https://www.docker.com/get-started/)
- Install [Qdrant](https://qdrant.tech/documentation/quick-start/):

    - run this command to pull the latest docker image: `docker pull qdrant/qdrant`
    - run this command to start the docker container:
       -    ```Bash
            docker run -p 6333:6333 -p 6334:6334 \
                -v $(pwd)/qdrant_storage:/qdrant/storage:z \
                qdrant/qdrant
            ```
## Setup
- create a 'outputData' folder in the root of the directory
- create a .env file in the root of the directory containing the following variable:
    - OPENAI_API_KEY 
- create a folder called 'inputData' outside of the root directory. It should be accessible with this path: `../inputData`. 
- clone this [repository](https://github.com/RapidReview-ai/testRepo) into the 'inputData' folder. 

## Running the app
- Enter the functions you want to test on in the testing.json file. And run evaluate_performance.py to see how well the model performs.
- Inside of main.py you can pass the repo_path variable to the get_function_data function to change the training data.
- run `python main.py` to run the whole app including, getting the data from the git repo, generating embeddings, creating the database, and running the query.
    - If you only want to run one of these steps, run the corresponding file on their own.
- You can run the tests by running `pyththon test_getFuntionData.py`

