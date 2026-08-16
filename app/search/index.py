from collections import defaultdict

from app.search.tokenizer import tokenize


class InvertedIndex:
    def __init__(self):
        # term -> {doc_id: term_frequency}
        self.index: dict[str, dict[str, int]] = defaultdict(dict)

        # doc_id -> original document content
        self.documents: dict[str, str] = {}

        # doc_id -> number of tokens
        self.document_lengths: dict[str, int] = {}

        self.total_document_length = 0

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def total_documents(self) -> int:
        return self.document_count

    @property
    def average_document_length(self) -> float:
        if self.document_count == 0:
            return 0.0

        return (
            self.total_document_length
            / self.document_count
        )

    def add_document(
        self,
        doc_id: str,
        content: str | list[str],
    ) -> None:
        """
        Add or update a document in the index.

        Accepts either raw source code or pre-tokenized content.
        """

        if doc_id in self.documents:
            self.remove_document(doc_id)

        if isinstance(content, str):
            original_content = content
            tokens = tokenize(content)
        else:
            tokens = content
            original_content = " ".join(tokens)

        term_frequencies: dict[str, int] = {}

        for token in tokens:
            term_frequencies[token] = (
                term_frequencies.get(token, 0) + 1
            )

        for term, frequency in term_frequencies.items():
            self.index[term][doc_id] = frequency

        self.documents[doc_id] = original_content

        document_length = len(tokens)

        self.document_lengths[doc_id] = document_length
        self.total_document_length += document_length

    def remove_document(
        self,
        doc_id: str,
    ) -> None:
        if doc_id not in self.documents:
            return

        old_length = self.document_lengths.pop(
            doc_id,
            0,
        )

        self.total_document_length -= old_length

        self.documents.pop(
            doc_id,
            None,
        )

        empty_terms = []

        for term, postings in self.index.items():
            postings.pop(
                doc_id,
                None,
            )

            if not postings:
                empty_terms.append(term)

        for term in empty_terms:
            del self.index[term]

    def get_postings(
        self,
        term: str,
    ) -> dict[str, int]:
        return self.index.get(
            term,
            {},
        )

    def get_document_frequency(
        self,
        term: str,
    ) -> int:
        return len(
            self.index.get(
                term,
                {},
            )
        )

    def get_document_length(
        self,
        doc_id: str,
    ) -> int:
        return self.document_lengths.get(
            doc_id,
            0,
        )