import streamlit as st
import requests
from dotenv import load_dotenv
import os
import codecs

load_dotenv()

url = os.getenv("API_URL")


st.title("Brujula Legal")

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
            url,
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
