# before starting the script, make sure chroma db container is running (docker-compose up -d --build)
# ATTENTION: this script is for loading documents into the chroma db from scratch (i.e. the db is empty)
import chromadb
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from utils.documentProcessor import documentProcessor
from chromadb.utils import embedding_functions
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import uuid
from tqdm import tqdm

## PARAMETERS
#####################

FILE_PATH = "raw-data/Dune.pdf"
EMBEDDING_MODEL_NAME = (
    "sentence-transformers/LaBSE"  # agnostic to the language of the text
)
COLLECTION_NAME = "commented-penal-code"

# initialize the chroma client
chromaClient = chromadb.HttpClient(
    host="localhost", port=8000, settings=Settings(allow_reset=True)
)

# resetting the db
chromaClient.reset()
print("WARNING: DB reset... ❗️")

# load and split the document/s into chunks
chunks = documentProcessor(filePath=FILE_PATH, chunkSize=700, chunkOverlap=0)
print("Document/s loaded and split into chunks... ✅")
print(f"Number of chunks: {len(chunks)}")
print("Printing an example chunk:")
print(chunks[22])

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
        ids=[str(uuid.uuid1())], metadatas=chunk.metadata, documents=chunk.page_content
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

# test the vector store
testDoc = langchainsChromaDB.similarity_search(
    "Que dice el articulo 35 del codigo penal?"
)
print(testDoc[0])
