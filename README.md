# Juribot

Question Answering Bot for legal documents, leveraging from the RAG technology.


## Directory Structure

```
.
├── .gitignore
├── README.md
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── models
│   │   │   └── chatModels.py
│   │   ├── services
│   │   │   ├── ragPipeline.py
│   │   │   ├── utils
│   │   │   │   ├── __init__.py
│   │   │   │   ├── documentProcessor.py
│   │   │   │   └── vectorDbLoaderHelper.py
│   │   │   └── vectorDbLoader.py
│   ├── scrapers
│   │   └── CSJN-scraper.ipynb
│   └── test
│       └── testCollection.py
└── frontend
    └── streamlitPrototype.py
```


## Testing the Application

### Setup: Loading documents into the Chroma Vectordatabase

Make sure to add the following change to the docker compose file in the chroma db repo within the environment variables: 

```
- ALLOW_RESET=TRUE
```

Before loading the documents to the DB, make sure the Chroma DB container is running:

- start your docker deamon and then run the following commands:

```sh
cd chroma
docker-compose up -d --build
```

### Preparation

Process the document you want to add to the rag pipeline

To load and split documents into chunks, run the `vectorDbLoader.py` script:

```sh
cd backend
python app/services/vectorDbLoader.py
```

This script loads a document from the specified file path, splits it into chunks, and stores the chunks in the Chroma DB.

### Run the backend

Execute the commands: 

```
cd app
uvicorn main:app --reload
```

### Making requests to the API

You can test the application by sending POST requests to the `/chain` endpoint. Here's an example Python script to test the application:

```python
import requests

data = {
    "message": "what is your name?",
    "chat_history": ""
}

response = requests.post("[hosting url]/chain", json=data)
print(response.text)
```

To continue the conversation, update the `message` and `chat_history` in the `data` dictionary and send another request.

## Unit Testing

Unit tests for the application are located in the `backend/test` directory. The main test file is [`testCollection.py`](backend/test/testCollection.py).

To run the tests, navigate to the `backend` directory and execute the following command:

```sh
python -m unittest test/testCollection.py
```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.