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
    ".ts",
    ".tsx",
    ".jsx",
}


class RepositoryLoader:
    def __init__(
        self,
        search_engine: SearchEngine,
    ):
        self.search_engine = search_engine

    def load(self, repository_path: str) -> int:
        root = Path(repository_path)

        if not root.exists():
            raise FileNotFoundError(
                f"Repository does not exist: {repository_path}"
            )

        indexed_files = 0

        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix not in SUPPORTED_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )
            except UnicodeDecodeError:
                continue

            relative_path = str(
                file_path.relative_to(root)
            )

            self.search_engine.add_document(
                relative_path,
                content,
            )

            indexed_files += 1

        return indexed_files