
from backend.retrieval import search_code

question = "How does the library send HTTP requests?"

results = search_code(question, top_k=5)

print(f"\nQuestion: {question}")
print(f"Results found: {len(results)}")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print(f"File: {result['path']}")
    print(
        f"Lines: {result['start_line']}-"
        f"{result['end_line']}"
    )
    print(f"Distance: {result['distance']:.4f}")
    print(result["content"][:500])
