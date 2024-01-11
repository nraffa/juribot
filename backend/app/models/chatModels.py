import queue
import threading
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.manager import AsyncCallbackManager
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from services.ragPipeline import ragChainInitializer


## PARAMETERS
############################################

NUMBER_OF_RESULTS_IN_SEARCH = 6

SEARCH_TYPE = "similarity"

############################################


class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration:
            raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)


class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)


def llm_thread(g, prompt, chat_history):
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=1000,
            streaming=True,
            callback_manager=AsyncCallbackManager([ChainStreamHandler(g)]),
        )
        ragChain = ragChainInitializer(llm, SEARCH_TYPE, NUMBER_OF_RESULTS_IN_SEARCH)

        ai_msg = ragChain.invoke({"question": prompt, "chat_history": chat_history})
        # TODO this should be handled from the frontend part later
        # (as at first it will be saved temporarily in the local client storage)
        chat_history.extend([HumanMessage(content=prompt), ai_msg])

    finally:
        g.close()


def chainThread(prompt, chat_history):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt, chat_history)).start()
    return g


class ChainRequest(BaseModel):
    message: str
    chat_history: str
