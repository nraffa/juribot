import streamlit as st
import requests
from dotenv import load_dotenv
import os
from utils.pdfViewer import tmpFileCreator, showPdf

load_dotenv()

url = os.getenv("API_URL")


st.title("Brujula Legal")

uploadedFile = st.file_uploader("Choose a file", type="pdf")


with st.sidebar:
    st.title("PDF Viewer")
    if uploadedFile is not None:
        # Create a temporary file and write the stream to it
        with st.spinner("Loading..."):
            tmpFileName = tmpFileCreator(uploadedFile)

            # Generate the iframe
            iframe = showPdf(tmpFileName)

        # Show the pdf
        st.markdown(iframe, unsafe_allow_html=True)

with st.spinner("Loading documents into the database..."):
    # here call the post request to api for uploading the document
    if uploadedFile is not None:
        with open(tmpFileName, "rb") as f:
            fileContent = f.read()

        files = {"file": ("filename", fileContent)}

        response = requests.post(url + "/upload", files=files)

        st.success(response.json()["message"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    data = {
        "message": prompt,
        "chat_history": "",
    }

    full_response = ""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with requests.post(
            url + "/chain",
            json=data,
            stream=True,
        ) as response:
            incomplete_chunk = b""
            for chunk in response.iter_content():
                try:
                    line = (incomplete_chunk + chunk).decode("utf-8")
                    incomplete_chunk = b""
                except UnicodeDecodeError:
                    incomplete_chunk += chunk
                    continue

                full_response += line

                message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
