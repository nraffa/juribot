from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from services.utils.dbLoaderHelper import vectorStoreLoader
from models.chatModels import chainThread, ChainRequest
from fastapi.middleware.cors import CORSMiddleware


# from .services.utils.filesHandling import tmpFileCreator

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
    request.chat_history = chat_history
    gen = chainThread(request.message, request.chat_history)
    return StreamingResponse(gen, media_type="text/event-stream")


@app.post("/upload")
async def _upload(file: UploadFile):
    # Save the uploaded PDF file to a desired location
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    try:
        vectorStoreLoader("chroma-db", 8000, path=file.filename)  # chroma-db
        return {"message": "Successfully uploaded the document to the database."}
    except Exception as e:
        return {"error": str(e)}
