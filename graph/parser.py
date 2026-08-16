import ast
from pathlib import Path

from graph.dependency_graph import DependencyGraph


class PythonDependencyParser:
    def __init__(self):
        self.graph = DependencyGraph()

    def parse_repository(
        self,
        repository_path: str,
    ) -> DependencyGraph:
        root = Path(repository_path)

        python_files = list(
            root.rglob("*.py")
        )

        modules = {}

        for file_path in python_files:
            relative = file_path.relative_to(root)

            module_name = ".".join(
                relative.with_suffix("").parts
            )

            modules[module_name] = str(relative)

        for module_name, relative_path in modules.items():
            full_path = root / relative_path

            try:
                source = full_path.read_text(
                    encoding="utf-8"
                )

                tree = ast.parse(source)

            except (
                UnicodeDecodeError,
                SyntaxError,
            ):
                continue

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported = alias.name

                        if imported in modules:
                            self.graph.add_dependency(
                                relative_path,
                                modules[imported],
                            )

                elif isinstance(
                    node,
                    ast.ImportFrom,
                ):
                    if node.module is None:
                        continue

                    imported = node.module

                    if imported in modules:
                        self.graph.add_dependency(
                            relative_path,
                            modules[imported],
                        )

        return self.graph