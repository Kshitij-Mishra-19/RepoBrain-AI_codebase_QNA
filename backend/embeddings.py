
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_model():
    """Load the embedding model once and reuse it."""
    global _model

    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convert text strings into embedding vectors."""
    if not texts:
        return []

    model = get_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()


if __name__ == "__main__":
    samples = [
        "Send an HTTP GET request",
        "Create a new HTTP session",
    ]

    vectors = embed_texts(samples)

    print(f"\nNumber of vectors: {len(vectors)}")
    print(f"Dimensions per vector: {len(vectors[0])}")
    print(f"First five values: {vectors[0][:5]}")

    assert len(vectors) == 2
    assert len(vectors[0]) == 384
    assert len(vectors[1]) == 384

    print("\nEmbedding test passed!")
