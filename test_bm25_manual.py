from app.search.index import InvertedIndex
from app.search.bm25 import BM25
from app.search.top_k import get_top_k


index = InvertedIndex()

index.add_document(
    "auth.py",
    [
        "authentication",
        "authentication",
        "authentication",
        "token",
        "token",
        "user",
    ],
)

index.add_document(
    "user.py",
    [
        "authentication",
        "user",
        "database",
        "profile",
        "settings",
    ],
)

index.add_document(
    "middleware.py",
    [
        "authentication",
        "token",
        "middleware",
        "request",
        "validation",
    ],
)

index.add_document(
    "payment.py",
    [
        "payment",
        "transaction",
        "database",
        "stripe",
        "refund",
    ],
)

bm25 = BM25(index)

query = ["authentication", "token"]

document_scores = {}

for document in index.document_lengths:
    document_scores[document] = bm25.score_query(
        query,
        document
    )

results = get_top_k(
    document_scores,
    k=2
)

for document, score in results:
    print(document, score)