from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from services.utils.dbInitializer import vectorStoreInitializer
import os

load_dotenv()

## PARAMETERS
############################################

os.environ["TOKENIZERS_PARALLELISM"] = "false"

############################################

CHROMADATABASE = vectorStoreInitializer("chroma-db", 8000)  # chroma-db

chat_history = []


def ragChainInitializer(llm, searchType, numberOfResultsInSearch, db=CHROMADATABASE):
    """
    Initializes a RAG (Retrieval-Augmented Generation) chain for document retrieval and question answering.

    This function sets up a RAG chain that uses a Chroma DB retriever to retrieve documents based on a question,
    and a language model to generate an answer based on the retrieved documents and the question.

    The retriever is configured with a specified search type and number of results to return.

    A prompt template is created from the specified template, and is used to format the question and documents into a prompt for the language model.

    The RAG chain is set up to run the retriever and language model in parallel. The documents returned by the retriever are used as the context for the language model.

    Parameters:
    llm (LanguageModel): The language model to use for generating answers.
    searchType (str): The search type to use for the retriever.
    numberOfResultsInSearch (int): The number of results to return from the retriever.
    template (str): The template to use for formatting the question and documents into a prompt.

    Returns:
    RunnableParallel: A RAG chain that can be used to retrieve documents and generate answers to questions.
    """

    if db is not None:
        retriever = db.as_retriever(
            search_type=searchType, search_kwargs={"k": numberOfResultsInSearch}
        )

    ## Defining the chat history chain
    ##########################################

    chatHistorySystemPrompt = """Given a chat history and the latest user question \
    which might reference the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is.
    """

    condenseChatHistoryPromptObj = ChatPromptTemplate.from_messages(
        [
            ("system", chatHistorySystemPrompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    condenseChatHistoryChain = condenseChatHistoryPromptObj | llm | StrOutputParser()

    ##########################################

    ## Defining the QA retrieval chain

    qaSystemPrompt = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible. 
    When giving an answer ALWAYS say where you found the answer (DOCUMENT and PAGE found in the metadata).
    {chat_history}
    {context}"""

    qaPromptObj = ChatPromptTemplate.from_messages(
        [
            ("system", qaSystemPrompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    ##########################################

    def condense_question(input: dict):
        # it seems this part is the one that generates double response
        # but if i take it out it doesn't know about the chat history
        # if input.get("chat_history"):
        #     return condenseChatHistoryChain
        # else:
        return input["question"]

    if db is not None:
        ragChain = (
            RunnablePassthrough.assign(context=condense_question | retriever)
            | qaPromptObj
            | llm
        )
    else:
        ragChain = (
            RunnablePassthrough.assign(context=condense_question) | qaPromptObj | llm
        )

    return ragChain
