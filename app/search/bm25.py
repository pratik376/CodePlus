import math

from app.search.index import InvertedIndex
from app.search.tokenizer import tokenize


class BM25:
    def __init__(
        self,
        index: InvertedIndex,
        k1: float = 1.5,
        b: float = 0.75,
    ):
        self.index = index
        self.k1 = k1
        self.b = b

    def _idf(self, term: str) -> float:
        total_documents = self.index.document_count
        document_frequency = self.index.document_frequency(term)

        if document_frequency == 0:
            return 0.0

        return math.log(
            1
            + (
                total_documents
                - document_frequency
                + 0.5
            )
            / (
                document_frequency
                + 0.5
            )
        )

    def score(
        self,
        query: str,
        doc_id: str,
    ) -> float:
        query_terms = tokenize(query)

        document_length = self.index.document_lengths[doc_id]
        average_length = self.index.average_document_length or 1.0

        total_score = 0.0

        for term in query_terms:
            postings = self.index.get_postings(term)

            term_frequency = postings.get(doc_id, 0)

            if term_frequency == 0:
                continue

            idf = self._idf(term)

            numerator = (
                term_frequency
                * (self.k1 + 1)
            )

            denominator = (
                term_frequency
                + self.k1
                * (
                    1
                    - self.b
                    + self.b
                    * document_length
                    / average_length
                )
            )

            total_score += (
                idf
                * numerator
                / denominator
            )

        return total_score