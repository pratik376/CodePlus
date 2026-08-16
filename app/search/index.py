from collections import Counter, defaultdict

from app.search.tokenizer import tokenize


class InvertedIndex:
    def __init__(self):
        self.documents: dict[str, str] = {}

        self.postings: dict[
            str,
            dict[str, int]
        ] = defaultdict(dict)

        self.document_lengths: dict[str, int] = {}

    def add_document(
        self,
        doc_id: str,
        content: str,
    ) -> None:
        if doc_id in self.documents:
            self.remove_document(doc_id)

        tokens = tokenize(content)

        self.documents[doc_id] = content
        self.document_lengths[doc_id] = len(tokens)

        frequencies = Counter(tokens)

        for term, frequency in frequencies.items():
            self.postings[term][doc_id] = frequency

    def remove_document(self, doc_id: str) -> None:
        if doc_id not in self.documents:
            return

        content = self.documents[doc_id]
        terms = set(tokenize(content))

        for term in terms:
            posting = self.postings.get(term)

            if posting is None:
                continue

            posting.pop(doc_id, None)

            if not posting:
                del self.postings[term]

        del self.documents[doc_id]
        self.document_lengths.pop(doc_id, None)

    def get_postings(
        self,
        term: str,
    ) -> dict[str, int]:
        return self.postings.get(term.lower(), {})

    def document_frequency(
        self,
        term: str,
    ) -> int:
        return len(self.get_postings(term))

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def average_document_length(self) -> float:
        if not self.document_lengths:
            return 0.0

        return (
            sum(self.document_lengths.values())
            / len(self.document_lengths)
        )