import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings


def checkCollection():
    EMBEDDING_MODEL_NAME = (
        "sentence-transformers/LaBSE"  # agnostic to the language of the text
    )
    COLLECTION_NAME = str(
        input("Enter the name of the chroma db collection: ")
    )  # "commented-penal-code"

    client = chromadb.HttpClient(
        host="localhost", port=8000, settings=Settings(allow_reset=True)
    )

    chromaClientEmbeddingFunction = (
        embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
    )

    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=chromaClientEmbeddingFunction,
    )

    print(collection.peek())


checkCollection()
