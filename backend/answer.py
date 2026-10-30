
import os

from dotenv import load_dotenv
from google import genai

from backend.retrieval import search_code

load_dotenv()

MODEL_NAME = "gemini-3.8-flash"


def answer_question(question: str, top_k: int = 5) -> str:
    if not question.strip():
        return "Please enter a question."

    # Retrieve relevant code from ChromaDB.
    results = search_code(
        question,
        top_k=top_k,
        source_only=False,
    )

    print(f"Retrieved {len(results)} code chunks.")
    print("Preparing context for Gemini...")

    if not results:
        return "No relevant code was found in the indexed repository."

    # Prepare code context with source locations.
    context_parts = []

    for i, result in enumerate(results, start=1):
        context_parts.append(
            f"Source {i}: {result['path']}\n"
            f"Lines: {result['start_line']}-"
            f"{result['end_line']}\n"
            f"Code:\n{result['content']}"
        )

    context = "\n\n".join(context_parts)

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "GEMINI_API_KEY was not found. "
            "Check that your project-root .env file contains "
            "GEMINI_API_KEY=your_actual_key."
        )

    # Initialize Gemini and generate an explanation.
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are RepoBrain, an assistant that explains GitHub repositories.

Answer the user's question using only the retrieved source context below.

Rules:
1. Explain the relevant code in beginner-friendly language.
2. Do not invent functions, behavior, or source locations.
3. Cite supporting code as `path/to/file.py: start-end`.
4. If the context is insufficient, say what cannot be determined.
5. Distinguish facts from reasonable inferences.

User question:
{question}

Retrieved source context:
{context}
"""

    response = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
    )

    print("Gemini response received.")

    if not response.output_text:
        return "Gemini returned an empty response. Please try again."

    return response.output_text


if __name__ == "__main__":
    question = input("Ask a question about the repository: ")

    import traceback

    try:
        print("\n" + answer_question(question))
    except Exception as exc:
        print(f"\nError while generating the answer: {exc}")
        traceback.print_exc()
