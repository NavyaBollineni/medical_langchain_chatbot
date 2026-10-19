
import json
from pathlib import Path
from langchain_core.documents import Document


# File paths
BASE_DIR = Path(__file__).parent

INPUT_PATH = BASE_DIR / "medical_data.json"
OUTPUT_PATH = BASE_DIR / "medical_chunks.json"


# Load JSON data
def load_data():

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# Create LangChain documents from records
def create_chunks(data):

    documents = []

    for sheet_name, records in data.items():

        for record_number, record in enumerate(records, start=1):

            # Convert one complete record into text
            content = "\n".join(
                f"{key}: {value}"
                for key, value in record.items()
            )

            # Create a LangChain Document
            document = Document(
                page_content=content,
                metadata={
                    "chunk_id": f"{sheet_name}_{record_number}",
                    "source": sheet_name,
                    "record_id": record_number
                }
            )

            documents.append(document)

    return documents


# Save LangChain documents as JSON
def save_chunks(documents):

    chunks_data = [
        {
            "chunk_id": document.metadata["chunk_id"],
            "source": document.metadata["source"],
            "record_id": document.metadata["record_id"],
            "content": document.page_content
        }
        for document in documents
    ]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            chunks_data,
            file,
            indent=4,
            ensure_ascii=False,
            allow_nan=False
        )


# Run the process
def main():

    data = load_data()
    documents = create_chunks(data)
    save_chunks(documents)


if __name__ == "__main__":
    main()
