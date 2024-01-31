import streamlit as st
from streamlit_authenticator import Authenticate
import requests
from dotenv import load_dotenv
import os
from utils.pdfViewer import tmpFileCreator, showPdf

import yaml
from yaml.loader import SafeLoader

load_dotenv()

url = os.getenv("API_URL")

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

# widget to enter username and password
authenticator.login()

# if user is authenticated, show content
if st.session_state["authentication_status"]:
    a, b, c, d = st.columns([3, 1, 1, 1])
    with d:
        authenticator.logout()
    with a:
        st.write(f'Welcome *{st.session_state["name"]}*')

    st.title("Brujula Legal")

    uploadedFile = st.file_uploader("Choose a file", type="pdf")

    # col1, col2, col3 = st.columns(3)

    # the button is necessary so that the code below is not executed every time the user interacts with the app
    # it seems the app get's refreshed every time the user interacts with it...
    # with b:
    if st.button("Db Upload"):
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
                fileContent = uploadedFile.read()

                files = {"file": ("filename", fileContent)}

                uploadResponse = requests.post(url + "/upload", files=files)

                try:
                    st.success(uploadResponse.json()["message"])
                except:
                    st.error(f"Eror uploading file: {uploadResponse.json()}")

    with c:
        if st.button("Clear chat"):
            st.session_state.messages = []
            # post request to delete-chat-history endpoint so that it gets deleted from the backend
            requests.post(url + "/delete-chat-history")

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

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

# if user is not authenticated, show error
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
# if user has not entered username and password, show warning
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
