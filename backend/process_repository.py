
from backend.ingest import clone_repository
from backend.extract import extract_files
from backend.chunking import chunk_file


def process_repository(repo_url: str) -> list[dict]:
    # Step 1: Download the repository
    repo_dir = clone_repository(repo_url)
    print(f"\nRepository downloaded: {repo_dir.name}")

    # Step 2: Extract supported files
    files = extract_files(repo_dir)
    print(f"Files extracted: {len(files)}")

    # Step 3: Split files into chunks
    all_chunks = []

    for file in files:
        chunks = chunk_file(
            path=file["path"],
            content=file["content"],
            chunk_lines=60,
            overlap=10,
        )
        all_chunks.extend(chunks)

    print(f"Total chunks created: {len(all_chunks)}")

    return all_chunks


if __name__ == "__main__":
    url = input("Enter a public GitHub repository URL: ").strip()

    try:
        chunks = process_repository(url)

        print("\n--- Sample chunks ---")

        for chunk in chunks[:3]:
            print(
                f"\nFile: {chunk['path']}"
                f"\nLines: {chunk['start_line']}-{chunk['end_line']}"
                f"\nContent preview:\n{chunk['content'][:250]}"
            )

        print("\nRepository processing completed successfully!")

    except (ValueError, RuntimeError) as exc:
        print(f"\nError: {exc}")
