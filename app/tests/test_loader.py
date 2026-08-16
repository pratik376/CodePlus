from app.repository.loader import RepositoryLoader
from app.search.engine import SearchEngine


def test_repository_loader(tmp_path):
    source = tmp_path / "auth.py"

    source.write_text(
        "def authenticate_user(token): return token",
        encoding="utf-8",
    )

    ignored = tmp_path / "notes.txt"

    ignored.write_text(
        "authentication documentation",
        encoding="utf-8",
    )

    engine = SearchEngine()
    loader = RepositoryLoader(engine)

    count = loader.load(str(tmp_path))

    assert count == 1
    assert engine.index.document_count == 1

    results = engine.search(
        "authenticate_user"
    )

    assert len(results) == 1
    assert results[0].doc_id == "auth.py"


def test_repository_loader_ignores_virtual_environment(tmp_path):
    app_directory = tmp_path / "app"
    app_directory.mkdir()

    source_file = app_directory / "main.py"

    source_file.write_text(
        "def run_application(): return True",
        encoding="utf-8",
    )

    venv_directory = (
        tmp_path
        / ".venv"
        / "Lib"
        / "site-packages"
    )

    venv_directory.mkdir(parents=True)

    dependency_file = (
        venv_directory
        / "dependency.py"
    )

    dependency_file.write_text(
        "def external_dependency(): return True",
        encoding="utf-8",
    )

    engine = SearchEngine()
    loader = RepositoryLoader(engine)

    count = loader.load(
        str(tmp_path)
    )

    assert count == 1

    assert (
        "app/main.py"
        in engine.index.documents
    )

    assert not any(
        ".venv" in document
        for document in engine.index.documents
    )