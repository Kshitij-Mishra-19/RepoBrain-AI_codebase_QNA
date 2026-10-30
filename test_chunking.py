
from backend.chunking import chunk_file

sample_code = "\n".join(
    f"print('Line {i}')" for i in range(1, 151)
)

chunks = chunk_file(
    path="example.py",
    content=sample_code,
    chunk_lines=60,
    overlap=10,
)

print("Total chunks:", len(chunks))

for chunk in chunks:
    print(
        f"{chunk['path']} | "
        f"Lines {chunk['start_line']}-{chunk['end_line']}"
    )

assert len(chunks) == 3
assert chunks[0]["start_line"] == 1
assert chunks[0]["end_line"] == 60
assert chunks[1]["start_line"] == 51
assert chunks[1]["end_line"] == 110
assert chunks[2]["start_line"] == 101
assert chunks[2]["end_line"] == 150

print("\nChunking test passed!")
