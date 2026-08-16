from app.repository.loader import RepositoryLoader
from app.search.engine import SearchEngine
from graph.parser import PythonDependencyParser


class RepositoryService:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.dependency_graph = None
        self.repository_path = None

    def index_repository(self, path: str) -> int:
        # Start fresh when indexing a new repository.
        self.search_engine = SearchEngine()

        loader = RepositoryLoader(
            self.search_engine
        )

        indexed_files = loader.load(path)

        parser = PythonDependencyParser()

        self.dependency_graph = (
            parser.parse_repository(path)
        )

        self.repository_path = path

        return indexed_files

    def search(
        self,
        query: str,
        limit: int = 10,
    ):
        return self.search_engine.search(
            query,
            limit,
        )

    def dependencies(self, file: str) -> list[str]:
        self._require_graph()

        return sorted(
            self.dependency_graph
            .transitive_dependencies(file)
        )

    def impact(self, file: str) -> tuple[list[str], list[str]]:
        self._require_graph()

        impacted = (
            self.dependency_graph
            .impact_analysis(file)
        )

        production_files = []
        test_files = []

        for impacted_file in impacted:
            normalized = impacted_file.replace(
                "\\",
                "/",
            )

            is_test = (
                "/tests/" in normalized
                or normalized.startswith("tests/")
                or normalized
                .split("/")[-1]
                .startswith("test_")
            )

            if is_test:
                test_files.append(impacted_file)
            else:
                production_files.append(impacted_file)

        return (
            sorted(production_files),
            sorted(test_files),
        )

    def has_cycle(self) -> bool:
        self._require_graph()

        return self.dependency_graph.has_cycle()

    def _require_graph(self):
        if self.dependency_graph is None:
            raise RuntimeError(
                "No repository has been indexed"
            )