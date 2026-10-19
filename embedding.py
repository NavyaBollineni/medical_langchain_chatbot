
import json
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings


# File paths
BASE_DIR = Path(__file__).parent

INPUT_PATH = BASE_DIR / "medical_chunks.json"
OUTPUT_PATH = BASE_DIR / "medical_embeddings.json"


# Load chunks from JSON
def load_chunks():

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# Generate embeddings using LangChain
def create_embeddings(chunks):

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    vectors = embedding_model.embed_documents(texts)

    embedded_chunks = []

    for chunk, vector in zip(chunks, vectors):

        embedded_chunks.append({
            **chunk,
            "embedding": vector
        })

    return embedded_chunks


# Save embeddings to JSON
def save_embeddings(embedded_chunks):

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            embedded_chunks,
            file,
            indent=4,
            ensure_ascii=False,
            allow_nan=False
        )


# Run the process
def main():

    chunks = load_chunks()
    embedded_chunks = create_embeddings(chunks)
    save_embeddings(embedded_chunks)


if __name__ == "__main__":
    main()
