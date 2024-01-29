# before starting the script, make sure chroma db container is running (docker-compose up -d --build)
# ATTENTION: this script is for loading documents into the chroma db from scratch (i.e. the db is empty)
import chromadb
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from services.utils.documentProcessor import documentProcessor, directoryProcessor
from chromadb.utils import embedding_functions
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import uuid
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

## PARAMETERS
#################################

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/LaBSE"  # agnostic to the language of the text
)
COLLECTION_NAME = "penalcode"

#################################


# function for processing and loading the chunks into the chroma db for the first time
def vectorStoreLoader(
    host: str,
    port: int,
    path: str = None,
):
    """
    Loads documents into a Chroma DB collection and returns a LangChain Chroma DB instance.

    This function initializes a Chroma DB client and resets the database. It then loads a document from a specified file path,
    splits it into chunks, and prints some information about the chunks.

    An embedding function is initialized using the SentenceTransformerEmbeddingFunction from the sentence-transformers library.
    A collection is created in the Chroma DB using this embedding function.

    The chunks are then added to the collection. Each chunk is given a unique ID, and its metadata and content are stored in the collection.

    Finally, a LangChain Chroma DB instance is created using the Chroma DB client, the collection name, and a SentenceTransformerEmbeddings function.

    Parameters:
    host (str): The host address of the Chroma DB.
    port (int): The port number of the Chroma DB.
    directory (bool): A boolean value indicating whether the input is a directory or not.
    path (str): The path of the file to be loaded into the Chroma DB.

    Returns:
    Chroma: A LangChain Chroma DB instance that can be used for further processing of the documents.

    Raises:
    Exception: If an error occurs while loading the documents, splitting them into chunks, or storing them in the Chroma DB.
    """
    # initialize the chroma client
    chromaClient = chromadb.HttpClient(
        host=host, port=port, settings=Settings(allow_reset=True)
    )

    # resetting the db
    chromaClient.reset()
    print("WARNING: DB reset... ❗️")

    # TODO add option for directory processing

    # if directory:
    #     DIRECTORY_PATH = str(
    #         input("Enter the path of the directory containing the documents: ")
    #     )
    #     # load and split the document/s into chunks
    #     chunks = directoryProcessor(
    #         directoryPath=DIRECTORY_PATH, chunkSize=700, chunkOverlap=0
    #     )
    #     print("Documents in folder has been loaded and split into chunks... ✅")
    #     print(f"Number of chunks: {len(chunks)}")
    # else:
    # load and split the document/s into chunks

    chunks = documentProcessor(filePath=path, chunkSize=700, chunkOverlap=0)
    print("Document/s loaded and split into chunks... ✅")
    print(f"Number of chunks: {len(chunks)}")

    # initialize the embedding function for chroma client
    chromaClientEmbeddingFunction = (
        embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
    )
    print("Embedding function initialized... ✅")

    # creating collection using custom embedding function from sentence-transformers library
    collection = chromaClient.create_collection(
        name=COLLECTION_NAME,
        embedding_function=chromaClientEmbeddingFunction,
    )
    print(f"Collection {COLLECTION_NAME} created... ✅")

    # adding chunks to collection
    print("Adding chunks to collection...")
    for chunk in tqdm(chunks):
        collection.add(
            ids=[str(uuid.uuid1())],
            metadatas=chunk.metadata,
            documents=chunk.page_content,
        )
    print("Chunks added to collection... ✅")

    # initialize the embedding function, this time for langchain wrapper
    langchainEmbeddingFunction = SentenceTransformerEmbeddings(
        model_name="sentence-transformers/LaBSE"
    )

    # tell LangChain to use our client and collection name
    langchainsChromaDB = Chroma(
        client=chromaClient,
        collection_name=COLLECTION_NAME,
        embedding_function=langchainEmbeddingFunction,
    )

    print("Script finished succesfully after loading documents into the chroma db... ✅")

    return langchainsChromaDB
