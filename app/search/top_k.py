import heapq


def get_top_k(
    document_scores: dict[str, float],
    k: int
) -> list[tuple[str, float]]:
    """
    Return the top K documents with the highest scores
    using a min-heap.
    """

    if k <= 0:
        return []

    heap = []

    for document_path, score in document_scores.items():
        if score <= 0:
            continue

        item = (score, document_path)

        if len(heap) < k:
            heapq.heappush(heap, item)

        elif score > heap[0][0]:
            heapq.heapreplace(heap, item)

    results = sorted(heap, reverse=True)

    return [
        (document_path, score)
        for score, document_path in results
    ]