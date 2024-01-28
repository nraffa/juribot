from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from services.utils.dbLoaderHelper import vectorStoreLoader
from models.chatModels import chainThread, ChainRequest
from fastapi.middleware.cors import CORSMiddleware
from services.ragPipeline import ragChainInitializer


chromaDatabase = None  # define as a global variable, possible issue if multiple processes try to use it at the same time

chat_history = []

app = FastAPI()

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chain")
def _chain(request: ChainRequest):
    global chromaDatabase  # Use the global chromaDatabase
    request.chat_history = chat_history
    gen = chainThread(request.message, request.chat_history, db=chromaDatabase)
    return StreamingResponse(gen, media_type="text/event-stream")


@app.post("/upload")
async def _upload(file: UploadFile):
    global chromaDatabase  # Use the global chromaDatabase

    # Save the uploaded PDF file to a desired location
    # vulnerability: path-injection Unvalidated input in path value creation risks unintended file/directory access
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    try:
        chromaDatabase = vectorStoreLoader("chroma-db", 8000, path=file.filename)

        return {"message": "Successfully uploaded the document to the database."}
    except Exception as e:
        return {"error": str(e)}
