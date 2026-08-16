from app.search.index import InvertedIndex


def test_add_document():
    index = InvertedIndex()

    index.add_document(
        "auth.py",
        "token token authentication",
    )

    postings = index.get_postings(
        "token"
    )

    assert postings["auth.py"] == 2


def test_remove_document():
    index = InvertedIndex()

    index.add_document(
        "auth.py",
        "token authentication",
    )

    index.remove_document(
        "auth.py"
    )

    assert (
        index.document_count
        == 0
    )

    assert (
        index.get_postings("token")
        == {}
    )


def test_update_document():
    index = InvertedIndex()

    index.add_document(
        "auth.py",
        "token token",
    )

    index.add_document(
        "auth.py",
        "authentication",
    )

    assert (
        index.get_postings("token")
        == {}
    )

    assert (
        index.get_postings(
            "authentication"
        )["auth.py"]
        == 1
    )