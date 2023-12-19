import streamlit as st
import requests


st.title("JuriBot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Talk to me"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"juri: {prompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        data = {"message": prompt, "chat_history": ""}

        response = requests.post("http://127.0.0.1:8000/chain", json=data)

        # for response in answer(
        messages = (
            [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        stream = (True,)

        full_response += response.text  # .choices[0].delta.content or ""
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
