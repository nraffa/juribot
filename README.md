# Juribot

Question Answering Bot for legal documents, leveraging from the RAG technology.


## Directory Structure

```
.
├── .gitignore
├── README.md
├── app
│   ├── main.py
│   ├── models
│   │   └── chatModels.py
│   ├── services
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── documentProcessor.py
│   │   │   └── vectorDbLoaderHelper.py
│   │   ├── ragPipeline.py
│   │   └── vectorDbLoader.py
└── notebooks
    ├── CSJN-scraper.ipynb
    ├── README.md
    ├── rag-pipeline-playground.ipynb
    └── random.ipynb
```

## Testing the Application

### Setup: Loading documents into the Chroma Vectordatabase

Before starting the script, make sure the Chroma DB container is running:

```sh
docker-compose up -d --build
```

### Preparation

Process the document you want to add to the rag pipeline

To load and split documents into chunks, run the `vectorDbLoader.py` script:

```sh
python app/services/vectorDbLoader.py
```

This script loads a document from the specified file path, splits it into chunks, and stores the chunks in the Chroma DB.

### Run the backend

Execute the command: 

```
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

## Notebooks

The `notebooks` directory contains Jupyter notebooks for data exploration and testing.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.