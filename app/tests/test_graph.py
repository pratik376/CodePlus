from graph.dependency_graph import (
    DependencyGraph,
)


def build_graph():
    graph = DependencyGraph()

    graph.add_dependency(
        "api.py",
        "auth.py",
    )

    graph.add_dependency(
        "auth.py",
        "database.py",
    )

    graph.add_dependency(
        "user.py",
        "database.py",
    )

    return graph


def test_dependencies():
    graph = build_graph()

    dependencies = (
        graph.transitive_dependencies(
            "api.py"
        )
    )

    assert "auth.py" in dependencies
    assert "database.py" in dependencies


def test_impact_analysis():
    graph = build_graph()

    impacted = graph.impact_analysis(
        "database.py"
    )

    assert "auth.py" in impacted
    assert "user.py" in impacted
    assert "api.py" in impacted


def test_cycle_detection():
    graph = DependencyGraph()

    graph.add_dependency("a.py", "b.py")
    graph.add_dependency("b.py", "c.py")
    graph.add_dependency("c.py", "a.py")

    assert graph.has_cycle()