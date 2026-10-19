
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Project paths
BASE_DIR = Path(__file__).parent
VECTOR_DB_PATH = BASE_DIR / "faiss_index"


# Store the vector database after loading it once
_vector_db = None


def load_vector_db():
    global _vector_db

    if _vector_db is None:
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            encode_kwargs={"normalize_embeddings": True}
        )

        _vector_db = FAISS.load_local(
            str(VECTOR_DB_PATH),
            embedding_model,
            allow_dangerous_deserialization=True
        )

    return _vector_db


def retrieve_chunks(question, k=3):
    if not question or not question.strip():
        return []

    vector_db = load_vector_db()

    retrieved_chunks = vector_db.similarity_search(
        question,
        k=k
    )

    return retrieved_chunks
