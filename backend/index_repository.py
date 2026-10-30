
from backend.ingest import clone_repository
from backend.extract import extract_files
from backend.chunking import chunk_file
from backend.retrieval import index_chunks, reset_collection

def index_repository(repo_url: str) -> int:
    print("\n[1/3] Downloading repository...")
    repo_dir = clone_repository(repo_url)
    print(f"Downloaded: {repo_dir.name}")

    print("\n[2/3] Extracting and chunking files...")
    files = extract_files(repo_dir)

    chunks = []
    for file in files:
        chunks.extend(
            chunk_file(
                path=file["path"],
                content=file["content"],
                chunk_lines=80,
                overlap=15,
            )
        )

    print(f"Files extracted: {len(files)}")
    print(f"Chunks created: {len(chunks)}")

    print("\n[3/3] Resetting the old index...")
    reset_collection()

    print("Creating embeddings and indexing...")
    total = index_chunks(chunks)

    print(f"Chunks indexed: {total}")
    return total


if __name__ == "__main__":
    url = input("Enter a public GitHub repository URL: ").strip()

    try:
        total = index_repository(url)
        print(f"\nIndexing completed! Total chunks: {total}")

    except (ValueError, RuntimeError) as exc:
        print(f"\nError: {exc}")
