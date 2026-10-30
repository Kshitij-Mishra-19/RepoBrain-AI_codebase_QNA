
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import shutil
import uuid

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def validate_github_url(repo_url: str) -> str:
    parsed = urlparse(repo_url.strip())

    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Enter a valid HTTPS GitHub URL.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) != 2 or not all(parts):
        raise ValueError(
            "Use: https://github.com/owner/repository"
        )

    owner, repo = parts

    if (
        any(part in {".", ".."} for part in parts)
        or "\\" in parsed.path
    ):
        raise ValueError("Invalid repository path.")

    if repo.endswith(".git"):
        repo = repo[:-4]

    return f"https://github.com/{owner}/{repo}.git"


def clone_repository(repo_url: str) -> Path:
    clean_url = validate_github_url(repo_url)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Use a fresh folder for every download.
    repo_dir = DATA_DIR / f"repository_{uuid.uuid4().hex[:8]}"

    try:
        subprocess.run(
            [
                "git",
                "-c", "core.hooksPath=/dev/null",
                "clone",
                "--depth", "1",
                "--single-branch",
                "--no-recurse-submodules",
                clean_url,
                str(repo_dir),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )

    except (subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        # Best-effort cleanup of this new folder only.
        shutil.rmtree(repo_dir, ignore_errors=True)
        raise RuntimeError(
            "Clone failed. Check the URL, Git installation, "
            "and internet connection."
        ) from exc

    return repo_dir


if __name__ == "__main__":
    url = input("Enter a public GitHub repository URL: ").strip()

    try:
        path = clone_repository(url)
        print("\nRepository downloaded successfully!")
        print(f"Location: {path}")

    except (ValueError, RuntimeError) as exc:
        print(f"\nError: {exc}")
