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
- Enter the function you want to test into the inputFunction.json file inside of the userInput folder.
- Inside of main.py you can pass the repo_path variable to the get_function_data function to change the training data.
- run `python main.py` to run the whole app including, getting the data from the git repo, generating embeddings, creating the database, and running the query.
    - If you only want to run one of these steps, run the corresponding file on their own.
- You can run the tests by running `pyththon test_getFuntionData.py`
