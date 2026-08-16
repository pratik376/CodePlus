from app.search.engine import SearchEngine


def test_relevant_document_ranks_first():
    engine = SearchEngine()

    engine.add_document(
        "auth.py",
        (
            "authenticate user token "
            "validate token authentication"
        ),
    )

    engine.add_document(
        "payment.py",
        (
            "calculate invoice payment "
            "total price"
        ),
    )

    results = engine.search(
        "authentication token"
    )

    assert results
    assert results[0].doc_id == "auth.py"


def test_limit():
    engine = SearchEngine()

    for number in range(20):
        engine.add_document(
            f"file_{number}.py",
            "authentication token",
        )

    results = engine.search(
        "authentication",
        limit=5,
    )

    assert len(results) == 5