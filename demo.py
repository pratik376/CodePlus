from app.repository.loader import RepositoryLoader
from app.search.engine import SearchEngine


def main():
    engine = SearchEngine()
    loader = RepositoryLoader(engine)

    indexed = loader.load(".")

    print(f"\nIndexed {indexed} source files.\n")

    while True:
        query = input("Search CodePulse (or 'exit'): ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results = engine.search(query, limit=5)

        if not results:
            print("No results found.\n")
            continue

        print()

        for position, result in enumerate(results, start=1):
            print(
                f"{position}. {result.doc_id} "
                f"(score={result.score:.3f})"
            )

        print()


if __name__ == "__main__":
    main()