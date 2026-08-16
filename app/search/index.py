from collections import defaultdict
from typing import Dict


class InvertedIndex:
    def __init__(self):
        # term -> {document_path: frequency}
        self.index: Dict[str, Dict[str, int]] = defaultdict(dict)

        # document_path -> total number of tokens
        self.document_lengths: Dict[str, int] = {}

        self.total_documents = 0
        self.total_document_length = 0

    def add_document(self, document_path: str, tokens: list[str]) -> None:
        """
        Add a tokenized document to the inverted index.
        """

        # If we're re-indexing an existing document,
        # remove the old version first.
        if document_path in self.document_lengths:
            self.remove_document(document_path)

        term_frequencies = {}

        for token in tokens:
            term_frequencies[token] = term_frequencies.get(token, 0) + 1

        for term, frequency in term_frequencies.items():
            self.index[term][document_path] = frequency

        document_length = len(tokens)

        self.document_lengths[document_path] = document_length
        self.total_documents += 1
        self.total_document_length += document_length

    def remove_document(self, document_path: str) -> None:
        """
        Remove a document and its statistics from the index.
        """

        if document_path not in self.document_lengths:
            return

        old_length = self.document_lengths.pop(document_path)

        self.total_documents -= 1
        self.total_document_length -= old_length

        empty_terms = []

        for term, postings in self.index.items():
            postings.pop(document_path, None)

            if not postings:
                empty_terms.append(term)

        for term in empty_terms:
            del self.index[term]

    def get_postings(self, term: str) -> Dict[str, int]:
        """
        Return documents containing the term and their term frequencies.
        """
        return self.index.get(term, {})

    def get_document_frequency(self, term: str) -> int:
        """
        Number of documents containing the term.
        """
        return len(self.index.get(term, {}))

    def get_document_length(self, document_path: str) -> int:
        return self.document_lengths.get(document_path, 0)

    @property
    def average_document_length(self) -> float:
        if self.total_documents == 0:
            return 0.0

        return self.total_document_length / self.total_documents