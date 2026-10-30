
from pathlib import Path
from backend.ingest import clone_repository


ALLOWED_EXTENSIONS = {
    ".py", ".java", ".js", ".jsx",
    ".ts", ".tsx", ".html", ".css",
    ".json", ".md", ".sql", ".kt",
}

IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv",
    "dist", "build", "__pycache__", ".next",
}

MAX_FILE_BYTES = 500_000


def extract_files(repo_dir: Path) -> list[dict]:
    documents = []

    for path in repo_dir.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(repo_dir)

        if any(part in IGNORED_DIRS for part in relative_path.parts):
            continue

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue

            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            if content.strip():
                documents.append({
                    "path": relative_path.as_posix(),
                    "content": content,
                })

        except OSError:
            continue

    return documents


if __name__ == "__main__":
    url = input("Enter a public GitHub repository URL: ").strip()

    try:
        repo_dir = clone_repository(url)
        files = extract_files(repo_dir)

        print(f"\nRepository: {repo_dir.name}")
        print(f"Total source files extracted: {len(files)}")

        for file in files[:10]:
            print(f"\nFile: {file['path']}")
            print(file["content"][:200])

    except (ValueError, RuntimeError) as exc:
        print(f"\nError: {exc}")
