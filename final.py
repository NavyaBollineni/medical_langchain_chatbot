
from retrieval import retrieve_chunks
from llm import generate_answer


def answer_question(question):
    retrieved_chunks = retrieve_chunks(question, k=3)

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    return answer


if __name__ == "__main__":
    question = input("Ask your medical appointment question: ")

    final_answer = answer_question(question)
    print(final_answer)
