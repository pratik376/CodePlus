from collections import defaultdict, deque


class DependencyGraph:
    def __init__(self):
        self.graph: dict[
            str,
            set[str]
        ] = defaultdict(set)

        self.reverse_graph: dict[
            str,
            set[str]
        ] = defaultdict(set)

    def add_dependency(
        self,
        source: str,
        dependency: str,
    ) -> None:
        self.graph[source].add(dependency)
        self.reverse_graph[dependency].add(source)

    def dependencies_of(
        self,
        node: str,
    ) -> set[str]:
        return self.graph.get(node, set())

    def dependents_of(
        self,
        node: str,
    ) -> set[str]:
        return self.reverse_graph.get(node, set())

    def transitive_dependencies(
        self,
        start: str,
    ) -> list[str]:
        visited = set()
        queue = deque([start])

        result = []

        while queue:
            current = queue.popleft()

            for neighbor in self.graph.get(current, set()):
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                result.append(neighbor)
                queue.append(neighbor)

        return result

    def impact_analysis(
        self,
        start: str,
    ) -> list[str]:
        visited = set()
        queue = deque([start])

        impacted = []

        while queue:
            current = queue.popleft()

            for dependent in self.reverse_graph.get(
                current,
                set(),
            ):
                if dependent in visited:
                    continue

                visited.add(dependent)
                impacted.append(dependent)
                queue.append(dependent)

        return impacted

    def has_cycle(self) -> bool:
        visited = set()
        recursion_stack = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            recursion_stack.add(node)

            for neighbor in self.graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True

                elif neighbor in recursion_stack:
                    return True

            recursion_stack.remove(node)
            return False

        all_nodes = set(self.graph)

        for dependencies in self.graph.values():
            all_nodes.update(dependencies)

        for node in all_nodes:
            if node not in visited:
                if dfs(node):
                    return True

        return False