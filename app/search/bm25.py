import math

from app.search.index import InvertedIndex


class BM25:
    def __init__(
        self,
        index: InvertedIndex,
        k1: float = 1.5,
        b: float = 0.75
    ):
        self.index = index
        self.k1 = k1
        self.b = b

    def idf(self, term: str) -> float:
        """
        Calculate inverse document frequency for a term.
        """

        total_documents = self.index.total_documents
        document_frequency = self.index.get_document_frequency(term)

        if document_frequency == 0:
            return 0.0

        return math.log(
            1
            + (
                total_documents - document_frequency + 0.5
            )
            / (
                document_frequency + 0.5
            )
        )

    def score(self, term: str, document_path: str) -> float:
        """
        Calculate the BM25 score for one term in one document.
        """

        postings = self.index.get_postings(term)

        if document_path not in postings:
            return 0.0

        term_frequency = postings[document_path]

        document_length = self.index.get_document_length(document_path)
        average_document_length = self.index.average_document_length

        if average_document_length == 0:
            return 0.0

        idf = self.idf(term)

        numerator = term_frequency * (self.k1 + 1)

        denominator = (
            term_frequency
            + self.k1
            * (
                1
                - self.b
                + self.b
                * (document_length / average_document_length)
            )
        )

        return idf * (numerator / denominator)

    def score_query(
        self,
        query_terms: list[str],
        document_path: str
    ) -> float:
        """
        Calculate the total BM25 score for multiple query terms
        against one document.
        """

        total_score = 0.0

        for term in query_terms:
            total_score += self.score(term, document_path)

        return total_score