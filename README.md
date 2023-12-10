# Juribot

Question Answering Bot for legal documents, leveraging from the RAG technology.

## Directory Structure

```
.
├── app
│   ├── main.py
│   └── services
│       ├── utils
│       │   ├── __init__.py
│       │   └── documentProcessor.py
│       └── vectorDbLoader.py
├── notebooks
│   ├── CSJN-scraper.ipynb
│   ├── README.md
│   ├── rag-pipeline-playground.ipynb
│   └── random.ipynb
└── .gitignore
```

## Loading documents into the Chroma Vectordatabase
### Setup

Before starting the script, make sure the Chroma DB container is running:

```sh
docker-compose up -d --build
```

### Usage

To load and split documents into chunks, run the `vectorDbLoader.py` script:

```sh
python app/services/vectorDbLoader.py
```

This script loads a document from the specified file path, splits it into chunks, and stores the chunks in the Chroma DB.

## Notebooks

The `notebooks` directory contains Jupyter notebooks for data exploration and testing.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.