
from backend.retrieval import search_code

question = "conn.urlopen("

results = search_code(
    question,
    top_k=5,
    source_only=True,
)

print(f"\nQuestion: {question}")
print(f"Source-code results: {len(results)}")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print(f"File: {result['path']}")
    print(
        f"Lines: {result['start_line']}-"
        f"{result['end_line']}"
    )
    print(f"Distance: {result['distance']:.4f}")
    print(f"Keyword score: {result['keyword_score']:.4f}")
    print(f"Combined score: {result['combined_score']:.4f}")
    print(result["content"][:300])
