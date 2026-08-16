from graph.dependency_graph import DependencyGraph
from graph.parser import PythonDependencyParser


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

    dependencies = graph.transitive_dependencies(
        "api.py"
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

    graph.add_dependency(
        "a.py",
        "b.py",
    )

    graph.add_dependency(
        "b.py",
        "c.py",
    )

    graph.add_dependency(
        "c.py",
        "a.py",
    )

    assert graph.has_cycle()


def test_parser_discovers_repository_dependencies(tmp_path):
    package = tmp_path / "services"
    package.mkdir()

    auth_file = package / "auth.py"
    database_file = package / "database.py"
    api_file = package / "api.py"

    database_file.write_text(
        "def find_user(user_id): return user_id",
        encoding="utf-8",
    )

    auth_file.write_text(
        (
            "from services.database import find_user\n\n"
            "def authenticate(user_id):\n"
            "    return find_user(user_id)\n"
        ),
        encoding="utf-8",
    )

    api_file.write_text(
        (
            "from services.auth import authenticate\n\n"
            "def get_user(user_id):\n"
            "    return authenticate(user_id)\n"
        ),
        encoding="utf-8",
    )

    parser = PythonDependencyParser()

    graph = parser.parse_repository(
        str(tmp_path)
    )

    auth_dependencies = graph.dependencies_of(
        "services/auth.py"
    )

    api_dependencies = graph.dependencies_of(
        "services/api.py"
    )

    assert "services/database.py" in auth_dependencies
    assert "services/auth.py" in api_dependencies