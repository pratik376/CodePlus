import heapq
from dataclasses import dataclass

from app.search.bm25 import BM25
from app.search.index import InvertedIndex
from app.search.tokenizer import tokenize


@dataclass
class SearchResult:
    doc_id: str
    score: float


class SearchEngine:
    def __init__(self):
        self.index = InvertedIndex()
        self.ranker = BM25(self.index)

    def add_document(
        self,
        doc_id: str,
        content: str,
    ) -> None:
        tokens = tokenize(content)
        self.index.add_document(
            doc_id,
            tokens,
        )

    def remove_document(
        self,
        doc_id: str,
    ) -> None:
        self.index.remove_document(doc_id)

    def search(
    self,
    query: str,
    limit: int = 10,
        ) -> list[SearchResult]:
        if not query.strip():
         return []

        query_terms = tokenize(query)

        candidate_documents: set[str] = set()

        for term in query_terms:
            candidate_documents.update(
                self.index
                .get_postings(term)
                .keys()
            )

        scored_documents = []

        for doc_id in candidate_documents:
            score = self.ranker.score_query(
                query_terms,
                doc_id,
            )

            if score > 0:
                scored_documents.append(
                    (
                        score,
                        doc_id,
                    )
                )

        top_results = heapq.nlargest(
            limit,
            scored_documents,
        )

        return [
            SearchResult(
                doc_id=doc_id,
                score=score,
            )
            for score, doc_id in top_results
        ]