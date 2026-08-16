from fastapi.testclient import TestClient

from main import app, service


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_index_and_search_repository(tmp_path):
    auth_file = tmp_path / "auth.py"

    auth_file.write_text(
        (
            "def authenticate_user(token):\n"
            "    return validate_token(token)\n\n"
            "def validate_token(token):\n"
            "    return bool(token)\n"
        ),
        encoding="utf-8",
    )

    response = client.post(
        "/repositories/index",
        json={
            "path": str(tmp_path)
        },
    )

    assert response.status_code == 200
    assert response.json()["indexed_files"] == 1

    response = client.post(
        "/search",
        json={
            "query": "authenticate_user",
            "limit": 5,
        },
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 1
    assert results[0]["file"] == "auth.py"


def test_dependency_endpoint(tmp_path):
    package = tmp_path / "services"
    package.mkdir()

    (package / "database.py").write_text(
        "def find_user(): return True",
        encoding="utf-8",
    )

    (package / "auth.py").write_text(
        (
            "from services.database "
            "import find_user\n"
        ),
        encoding="utf-8",
    )

    response = client.post(
        "/repositories/index",
        json={
            "path": str(tmp_path)
        },
    )

    assert response.status_code == 200

    response = client.get(
        "/dependencies",
        params={
            "file": "services/auth.py"
        },
    )

    assert response.status_code == 200

    assert (
        "services/database.py"
        in response.json()["dependencies"]
    )


def test_missing_repository_returns_404():
    response = client.post(
        "/repositories/index",
        json={
            "path": (
                "this-directory-"
                "definitely-does-not-exist"
            )
        },
    )

    assert response.status_code == 404


def test_dependencies_before_index_returns_409():
    service.dependency_graph = None

    response = client.get(
        "/dependencies",
        params={
            "file": "auth.py"
        },
    )

    assert response.status_code == 409