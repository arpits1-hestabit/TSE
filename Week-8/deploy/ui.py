import streamlit as st
import requests
import uuid

BACKEND_URL = "http://127.0.0.1:9000"

st.set_page_config(page_title="LLM UI", layout="wide")
st.title("Local GGUF LLM Interface")

#to mentain chat history across interactions
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Used for selecting the mode for the UI
mode = st.radio("Mode", ["generate", "chat"], horizontal=True)

# Controls for temperature, top_p, max_tokens, stream
col1, col2, col3 = st.columns(3)
with col1:
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7)
with col2:
    top_p = st.slider("Top-p", 0.1, 1.0, 0.95)
with col3:
    max_tokens = st.number_input("Max tokens", 32, 2048, 256)

stream = st.checkbox("Stream output", value=True)

# if mode =  "generate"
if mode == "generate":
    prompt = st.text_area("Prompt", height=150)

    if st.button("Generate"):
        payload = {
            "request_id": str(uuid.uuid4()),
            "prompt": prompt,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        endpoint = BACKEND_URL + "/generate"
        output_box = st.empty()
        output = ""

        if stream:
            with requests.post(endpoint, json=payload, stream=True) as r:
                for line in r.iter_lines():
                    if not line:
                        continue
                    text = line.decode().replace("data: ", "")
                    if text == "[DONE]":
                        break
                    output += text
                    output_box.markdown(output)
        else:
            r = requests.post(endpoint, json=payload)
            st.markdown(r.json().get("output", ""))

# if mode = "chat"
if mode == "chat":

    # Used for displaying the chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input to let the user enter messages
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Add user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # Prepare payload
        payload = {
            "request_id": str(uuid.uuid4()),
            "messages": st.session_state.chat_history,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        endpoint = BACKEND_URL + "/chat"

        assistant_placeholder = st.empty()
        assistant_reply = ""

        # Streaming response
        if stream:
            with requests.post(endpoint, json=payload, stream=True) as r:
                for line in r.iter_lines():
                    if not line:
                        continue
                    text = line.decode().replace("data: ", "")
                    if text == "[DONE]":
                        break
                    assistant_reply += text
                    assistant_placeholder.markdown(assistant_reply)
        else:
            r = requests.post(endpoint, json=payload)
            assistant_reply = r.json().get("output", "")
            assistant_placeholder.markdown(assistant_reply)

        # Save assistant message
        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_reply}
        )

    # To clear the chat history
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()
