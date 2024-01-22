from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from models.chatModels import chainThread, ChainRequest
from models.documentUploadModels import DocumentUploadRequest
from fastapi.middleware.cors import CORSMiddleware
from .services.dbLoader import vectorStoreLoader
from .services.utils.filesHandling import tmpFileCreator

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
async def _upload(file: UploadFile):  # DocumentUploadRequest):
    # get the file name from the request
    path = file.filename

    # # get the file name from the request
    # path = request.fileName
    # file = request.file

    # tmpFileName = await tmpFileCreator(file)

    vectorStoreLoader("chroma-db", 8000, path=path)

    return {"message": "Document uploaded successfully!"}
