
def chunk_file(
    path: str,
    content: str,
    chunk_lines: int = 60,
    overlap: int = 10,
) -> list[dict]:
    if chunk_lines <= 0:
        raise ValueError("chunk_lines must be positive")

    if overlap < 0 or overlap >= chunk_lines:
        raise ValueError("overlap must be between 0 and chunk_lines - 1")

    lines = content.splitlines()
    chunks = []
    start = 0

    while start < len(lines):
        end = min(start + chunk_lines, len(lines))

        # Prefer ending at a blank line near the chunk boundary.
        if end < len(lines):
            search_start = max(start + 1, end - 10)

            for i in range(end - 1, search_start - 1, -1):
                if not lines[i].strip():
                    end = i + 1
                    break

        chunk_content = "\n".join(lines[start:end])

        if chunk_content.strip():
            chunks.append({
                "id": f"{path}:{start + 1}-{end}",
                "path": path,
                "start_line": start + 1,
                "end_line": end,
                "content": chunk_content,
            })

        if end == len(lines):
            break

        # Ensure the next chunk starts after the previous start.
        start = max(start + 1, end - overlap)

    return chunks
