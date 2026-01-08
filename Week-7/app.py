import streamlit as st
import requests
from PIL import Image
import io

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Enterprise RAG UI", layout="wide")
st.title("Enterprise RAG | Image | SQL Interface")

st.sidebar.title("Choose Endpoint")
endpoint = st.sidebar.radio(
    "Select the functionality:",
    ["Text Search", "Image Search", "SQL Query"]
)

if endpoint == "Text Search":
    st.header("Text Search (/ask)")
    query = st.text_area("Enter your query")
    top_k = st.slider("Top K results", min_value=1, max_value=20, value=5)
    
    if st.button("Search"):
        if not query.strip():
            st.warning("Please enter a query")
        else:
            try:
                response = requests.post(
                    f"{BASE_URL}/ask",
                    json={"query": query, "top_k": top_k}
                )
                results = response.json()
                st.subheader("Results")
                st.json(results)
            except Exception as e:
                st.error(f"Error: {e}")

elif endpoint == "Image Search":
    st.header("Image Search (/ask-image)")
    mode = st.selectbox("Select mode", ["text_to_image", "text_to_text", "image_to_image", "image_to_text"])
    query = st.text_area("Query (for text-based modes)")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    top_k = st.slider("Top K results", min_value=1, max_value=20, value=5)

    if st.button("Search"):
        form_data = {
            "mode": mode,
            "top_k": top_k
        }
        if query.strip():
            form_data["query"] = query.strip()
        
        files = {}
        if uploaded_file is not None:
            files["image"] = (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)

        try:
            response = requests.post(f"{BASE_URL}/ask-image", data=form_data, files=files)
            results = response.json()
            st.subheader("Results")
            
            # Display images if returned
            if mode in ["text_to_image", "image_to_image"] and "results" in results:
                for r in results["results"]:
                    if "image_path" in r:
                        st.image(r["image_path"], width=300)
            else:
                st.json(results)
        except Exception as e:
            st.error(f"Error: {e}")

elif endpoint == "SQL Query":
    st.header("SQL Query (/ask-sql)")
    question = st.text_area("Enter your natural language question")

    if st.button("Run SQL"):
        if not question.strip():
            st.warning("Please enter a question")
        else:
            try:
                response = requests.post(f"{BASE_URL}/ask-sql", json={"question": question.strip()})
                results = response.json()
                st.subheader("SQL Execution Results")
                
                # Display SQL, results, summary nicely
                if "sql" in results:
                    st.markdown(f"**Generated SQL:**\n```sql\n{results['sql']}\n```")
                if "results" in results and results["results"]:
                    st.table(results["results"])
                if "summary" in results:
                    st.markdown(f"**Summary:** {results['summary']}")
                if "explanation" in results:
                    st.markdown(f"**Explanation:** {results['explanation']}")
            except Exception as e:
                st.error(f"Error: {e}")
