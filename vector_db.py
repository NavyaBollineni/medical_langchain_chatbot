
import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ---------------------------------
# 1. Define file paths
# ---------------------------------

BASE_DIR = Path(__file__).parent

CHUNK_PATH = BASE_DIR / "medical_chunks.json"
VECTOR_DB_PATH = BASE_DIR / "faiss_index"


# ---------------------------------
# 2. Load chunks from JSON
# ---------------------------------

def load_chunks():

    with open(CHUNK_PATH, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    return chunks


# ---------------------------------
# 3. Convert chunks into Documents
# ---------------------------------

def create_documents(chunks):

    documents = []

    for chunk in chunks:

        document = Document(
            page_content=chunk["content"],
            metadata={
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "record_id": chunk["record_id"]
            }
        )

        documents.append(document)

    return documents


# ---------------------------------
# 4. Create embedding model
# ---------------------------------

def create_embedding_model():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={
            "normalize_embeddings": True
        }
    )


# ---------------------------------
# 5. Create and save FAISS vector database
# ---------------------------------

def create_vector_db(documents, embedding_model):

    vector_db = FAISS.from_documents(
        documents,
        embedding_model
    )

    vector_db.save_local(str(VECTOR_DB_PATH))

    return vector_db


# ---------------------------------
# 6. Run the complete process
# ---------------------------------

def main():

    chunks = load_chunks()

    documents = create_documents(chunks)

    embedding_model = create_embedding_model()

    create_vector_db(documents, embedding_model)


if __name__ == "__main__":
    main()
