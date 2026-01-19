import streamlit as st
import requests
from collections import deque
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.memory_store import MemoryStore

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="RAG Assistant", layout="wide")

# Initialize session state for memory
if 'memory_store' not in st.session_state:
    st.session_state.memory_store = MemoryStore()

st.title("RAG Assistant")
st.write("Ask questions using text, images, or a database.")

mode = st.selectbox(
    "Select what you want to do",
    ["Text RAG", "Image RAG", "SQL RAG"]
)

st.divider()

# Display recent questions in sidebar
with st.sidebar:
    st.subheader("Last 5 Questions:")
    history = st.session_state.memory_store.get_question_history()
    
    if history:
        for idx, item in enumerate(history, 1):
            with st.container():
                st.markdown(f"**{idx}. [{item['mode']}]**")
                st.caption(item['question'][:50] + "..." if len(item['question']) > 50 else item['question'])
                st.caption(f"{item['timestamp'].split('T')[1][:5]}")
                st.divider()
    else:
        st.info("No questions asked yet.")

if mode == "Text RAG":
    st.header("Text Question Answering")

    question = st.text_area(
        "Enter your question",
        height=100
    )

    if st.button("Ask"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            st.session_state.memory_store.add_question(question, "Text RAG")
            with st.spinner("Thinking..."):
                resp = requests.post(
                    f"{API_BASE}/ask",
                    params={"question": question},
                    timeout=600,
                )

                data = resp.json()
                st.success("Answer")
                st.write(data.get("answer", ""))
                if "score" in data:
                    st.text(f"Faithfulness score: {data['score']}")

elif mode == "Image RAG":
    st.header("Image Question Answering")

    question = st.text_area(
        "Enter a question (optional)",
        height=80
    )

    image = st.file_uploader(
        "Upload an image",
        type=["jpg", "png", "jpeg"]
    )

    if st.button("Ask with Image"):
        if not image and question.strip() == "":
            st.warning("Upload an image or enter a question.")
        else:
            query_text = question if question.strip() else "[Image Query]"
            st.session_state.memory_store.add_question(query_text, "Image RAG")
            with st.spinner("Processing..."):
                data = {"top_k": 5}
                files = {}

                if question.strip():
                    data["question"] = question

                if image:
                    files["image"] = (
                        image.name,
                        image.getvalue(),
                        image.type,
                    )

                resp = requests.post(
                    f"{API_BASE}/ask-image",
                    data=data,
                    files=files,
                    timeout=1000,
                )

                result = resp.json()
                st.success("Answer")
                st.write(result.get("answer", ""))

                if "score" in result:
                    st.text(f"Faithfulness score: {result['score']}")

else:
    st.header("SQL Assistant")

    question = st.text_area(
        "Ask a question about the database",
        height=100
    )

    if st.button("Run Query"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            st.session_state.memory_store.add_question(question, "SQL RAG")
            st.write("Running SQL query...")
            response = requests.post(
                f"{API_BASE}/ask-sql",
                params={"question": question}
            )

            result = response.json()
            st.subheader("Result")
            st.write(result.get("summary", "No result found"))
