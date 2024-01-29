# Juribot

Question Answering Bot for legal documents, leveraging from the RAG technology.


## Directory Structure

```
.
├── .gitignore
├── README.md
├── docker-compose.yml
├── backend/
│   ├── .cache/
│   ├── Dockerfile
│   ├── app/
│   ├── requirements.txt
│   ├── scrapers/
│   ├── test/
│   └── .env
├── chroma/
│   └── ...
└── frontend/
    ├── Dockerfile
    ├── streamlitPrototype.py
    ├── requirements.txt
    └── .env
```




## Installation

This project uses Docker Compose to manage its services. To get started, you'll need to have Docker installed on your machine.

1. Clone the repository:

```bash
git clone https://github.com/nraffa/juribot.git
```

2. Navigate to the project directory:

```bash
cd juribot
```

3. Create environment files for the backend and frontend services:


For the backend, create a `.env` file in the `backend/` directory with the following variables:

```bash
# backend/.env
OPENAI_API_KEY={API_SECRET}
```

For the frontend, create a `.env` file in the `frontend/` directory with the following variables:

```bash
# frontend/.env
API_URL='http://backend:5000/chain'
```

4. Build and start the Docker services 

```bash
docker-compose up --build
```

## Usage
Once the Docker services are up and running, you can access the application at http://localhost:8501 .

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

### Making requests directly to the API

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

Another alternative is accessing the `Swagger Ui` endpoint in the hosting url for example: `http://127.0.0.1:8000/docs` and use the UI for playing around with the API.

## Unit Testing

Unit tests for the application are located in the `backend/test` directory. The main test file is [`testCollection.py`](backend/test/testCollection.py).

To run the tests, navigate to the `backend` directory and execute the following command:

```sh
python -m unittest test/testCollection.py
```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.