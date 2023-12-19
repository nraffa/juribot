from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def documentProcessor(filePath: str, chunkSize: int, chunkOverlap: int) -> list:
    """
    Processes a document by loading it and splitting it into chunks.

    This function uses the PyPDFLoader to load a PDF document from a given file path.
    It then uses the RecursiveCharacterTextSplitter to split the loaded document into chunks of text.
    The size of the chunks and the overlap between them can be specified.

    Parameters:
    filePath (str): The path to the PDF document to be processed.
    chunkSize (int): The desired size of the text chunks. This is the maximum number of characters that a chunk can contain.
    chunkOverlap (int): The desired overlap between the text chunks. This is the number of characters that consecutive chunks will overlap.

    Returns:
    list: A list of text chunks if the document is successfully loaded and split, None otherwise.

    Raises:
    Exception: If an error occurs while loading or splitting the document.
    """

    # Load the document
    documentLoader = PyPDFLoader(file_path=filePath)

    # initialize the text splitter
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=chunkSize, chunk_overlap=chunkOverlap
    )

    # Load the document and split it into chunks
    try:
        chunks = documentLoader.load_and_split(textSplitter)
        return chunks
    except Exception as e:
        print(e)
        return e


def directoryProcessor(directoryPath: str, chunkSize: int, chunkOverlap: int) -> list:
    """
    Processes all documents in a directory by loading them and splitting them into chunks.

    This function uses the DirectoryLoader to load all PDF documents from a given directory path.
    It then uses the RecursiveCharacterTextSplitter to split the loaded documents into chunks of text.
    The size of the chunks and the overlap between them can be specified.

    Parameters:
    directoryPath (str): The path to the directory containing the PDF documents to be processed.
    chunkSize (int): The desired size of the text chunks. This is the maximum number of characters that a chunk can contain.
    chunkOverlap (int): The desired overlap between the text chunks. This is the number of characters that consecutive chunks will overlap.

    Returns:
    list: A list of text chunks if the documents are successfully loaded and split, None otherwise.

    Raises:
    Exception: If an error occurs while loading or splitting the documents.
    """

    # Load the document
    documentLoader = DirectoryLoader(
        path=directoryPath,
        show_progress=True,
        use_multithreading=True,
        loader_cls=PyPDFLoader,
    )

    # initialize the text splitter
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=chunkSize, chunk_overlap=chunkOverlap
    )

    # Load the document and split it into chunks
    try:
        chunks = documentLoader.load_and_split(textSplitter)
        return chunks
    except Exception as e:
        print(e)
        return None
