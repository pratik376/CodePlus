from pathlib import Path

from app.search.engine import SearchEngine


SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".cpp",
    ".cc",
    ".c",
    ".h",
    ".hpp",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
}


class RepositoryLoader:
    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine

    def _should_ignore(self, path: Path, root: Path) -> bool:
        try:
            relative_path = path.relative_to(root)
        except ValueError:
            return True

        return any(
            part.lower() in IGNORED_DIRECTORIES
            for part in relative_path.parts
        )

    def load(self, repository_path: str) -> int:
        root = Path(repository_path).resolve()

        if not root.exists():
            raise FileNotFoundError(
                f"Repository not found: {repository_path}"
            )

        if not root.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {repository_path}"
            )

        indexed_files = 0

        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue

            if self._should_ignore(file_path, root):
                continue

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )
            except (
                UnicodeDecodeError,
                PermissionError,
                OSError,
            ):
                continue

            relative_path = (
                file_path
                .relative_to(root)
                .as_posix()
            )

            self.search_engine.add_document(
                relative_path,
                content,
            )

            indexed_files += 1

        return indexed_files