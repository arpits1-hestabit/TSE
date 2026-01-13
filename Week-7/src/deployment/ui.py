import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="RAG Assistant")

st.title("RAG Assistant")
st.write("Ask questions using text, images, or a database.")

mode = st.selectbox(
    "Select what you want to do",
    ["Text RAG", "Image RAG", "SQL RAG"]
)

st.divider()

if mode == "Text RAG":
    st.header("Text Question Answering")

    question = st.text_area(
        "Enter your question",
        height=100
    )

    if st.button("Ask"):
        if question.strip() == "":
            st.warning("Please enter a question.")
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
            st.write("Running SQL query...")
            response = requests.post(
                f"{API_BASE}/ask-sql",
                params={"question": question}
            )

            result = response.json()
            st.subheader("Result")
            st.write(result.get("summary", "No result found"))
