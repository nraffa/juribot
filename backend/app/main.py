from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from models.chatModels import chainThread, ChainRequest
from fastapi.middleware.cors import CORSMiddleware

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


# while True:
#     question = input("\nQuestion: ")

#     if question == "exit":
#         break

#     for chunk in chainThread(question, chat_history):
#         print(chunk, end="", flush=True)
