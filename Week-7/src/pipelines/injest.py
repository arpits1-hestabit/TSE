import os, json
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

RAW_DIR = "src/data/raw" # for injesting the raw documents
CHUNK_DIR = "src/data/chunks" # for saving the chunked documents
OUT_FILE = os.path.join(CHUNK_DIR, "text_chunks.jsonl") # output file for chunks (os.path.join is used as other files will be saved in the same folder)

os.makedirs(CHUNK_DIR, exist_ok=True) # it ensures that the chunk directory exists

# this function will load the documents based on their file type
def load_document(path):
    if path.endswith(".pdf"):
        return PyMuPDFLoader(path).load()
    elif path.endswith(".txt"):
        return TextLoader(path).load()
    elif path.endswith(".csv"):
        return CSVLoader(path).load()
    elif path.endswith(".docx"):
        return UnstructuredWordDocumentLoader(path).load()
    else:
        return []

# this is the main injestion function that processes all the files, splits them into chunks, adn then saves them
def ingest():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for file in os.listdir(RAW_DIR):
            path = os.path.join(RAW_DIR, file)
            docs = load_document(path)

            chunks = splitter.split_documents(docs)

            for i, c in enumerate(chunks): # enumerate is a built-in function and it is used to get the index for chunk_id
                record = {
                    "chunk_id": f"{file}_{i}",
                    "text": c.page_content,
                    # this metadata will overwrite the loader metadata and add more information
                    "metadata": {
                        "source": file,
                        "page": c.metadata.get("page"),
                        "type": file.split(".")[-1]
                    }
                }
                f.write(json.dumps(record) + "\n") # json.dumps converts the python object into a json formatted string

# run the injestion when this script is executed directly
if __name__ == "__main__":
    ingest()





