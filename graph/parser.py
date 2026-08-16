import ast
from pathlib import Path

from graph.dependency_graph import DependencyGraph


class PythonDependencyParser:
    def __init__(self):
        self.graph = DependencyGraph()

    def parse_repository(self, repository_path: str) -> DependencyGraph:
        root = Path(repository_path).resolve()

        modules = self._discover_modules(root)

        for module_name, relative_path in modules.items():
            full_path = root / relative_path

            try:
                source = full_path.read_text(encoding="utf-8")
                tree = ast.parse(source)

            except (UnicodeDecodeError, SyntaxError, OSError):
                continue

            self._process_imports(
                source_module=module_name,
                source_path=relative_path,
                tree=tree,
                modules=modules,
            )

        return self.graph

    def _discover_modules(
        self,
        root: Path,
    ) -> dict[str, str]:

        modules = {}

        ignored_directories = {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            ".pytest_cache",
        }

        for file_path in root.rglob("*.py"):

            relative = file_path.relative_to(root)

            if any(
                part.lower() in ignored_directories
                for part in relative.parts
            ):
                continue

            module_parts = list(
                relative.with_suffix("").parts
            )

            if module_parts[-1] == "__init__":
                module_parts = module_parts[:-1]

            if not module_parts:
                continue

            module_name = ".".join(module_parts)

            modules[module_name] = relative.as_posix()

        return modules

    def _process_imports(
        self,
        source_module: str,
        source_path: str,
        tree: ast.AST,
        modules: dict[str, str],
    ) -> None:

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    dependency = self._resolve_module(
                        alias.name,
                        modules,
                    )

                    if dependency:
                        self.graph.add_dependency(
                            source_path,
                            dependency,
                        )

            elif isinstance(node, ast.ImportFrom):

                if node.module is None:
                    continue

                dependency = self._resolve_module(
                    node.module,
                    modules,
                )

                if dependency:
                    self.graph.add_dependency(
                        source_path,
                        dependency,
                    )

    @staticmethod
    def _resolve_module(
        imported_module: str,
        modules: dict[str, str],
    ) -> str | None:

        if imported_module in modules:
            return modules[imported_module]

        parts = imported_module.split(".")

        while len(parts) > 1:
            parts.pop()

            candidate = ".".join(parts)

            if candidate in modules:
                return modules[candidate]

        return None