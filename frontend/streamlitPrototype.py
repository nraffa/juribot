import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("API_URL")


st.title("JuriBot")

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

    response = requests.post(url, json=data)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = response.text  # get_stream(url, data)
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
