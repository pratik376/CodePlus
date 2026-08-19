import argparse
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.repository_service import RepositoryService


QUERIES = [
    "repository",
    "search",
    "dependency",
    "parser",
    "test",
]

INDEXING_RUNS = 5
SEARCH_RUNS_PER_QUERY = 100

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
}


def percentile(values, p):
    ordered = sorted(values)

    index = int(
        (p / 100) * (len(ordered) - 1)
    )

    return ordered[index]


def count_python_lines(repository_path):
    total_lines = 0

    for path in repository_path.rglob("*.py"):
        if any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        ):
            continue

        try:
            with path.open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                total_lines += sum(1 for _ in file)
        except OSError:
            continue

    return total_lines


def benchmark_indexing(repository_path):
    latencies = []
    indexed_files = 0
    final_service = None

    for run in range(INDEXING_RUNS):
        service = RepositoryService()

        start = time.perf_counter()

        indexed_files = service.index_repository(
            str(repository_path)
        )

        elapsed = time.perf_counter() - start

        latencies.append(elapsed)

        final_service = service

        print(
            f"Indexing run {run + 1}/{INDEXING_RUNS}: "
            f"{elapsed:.3f} s"
        )

    return final_service, indexed_files, latencies


def benchmark_search(service):
    results = {}

    for query in QUERIES:
        # Warm-up search.
        service.search(query, limit=10)

        latencies = []

        for _ in range(SEARCH_RUNS_PER_QUERY):
            start = time.perf_counter()

            service.search(
                query,
                limit=10,
            )

            elapsed = time.perf_counter() - start

            latencies.append(elapsed * 1000)

        results[query] = latencies

    return results


def print_search_statistics(search_results):
    all_latencies = [
        latency
        for latencies in search_results.values()
        for latency in latencies
    ]

    print("\nSearch Performance")
    print("-" * 50)

    print(
        f"Total searches:      "
        f"{len(all_latencies):,}"
    )
    print(
        f"Average latency:     "
        f"{statistics.mean(all_latencies):.3f} ms"
    )
    print(
        f"P50 latency:         "
        f"{statistics.median(all_latencies):.3f} ms"
    )
    print(
        f"P95 latency:         "
        f"{percentile(all_latencies, 95):.3f} ms"
    )
    print(
        f"P99 latency:         "
        f"{percentile(all_latencies, 99):.3f} ms"
    )
    print(
        f"Min latency:         "
        f"{min(all_latencies):.3f} ms"
    )
    print(
        f"Max latency:         "
        f"{max(all_latencies):.3f} ms"
    )

    print("\nPer-query Performance")
    print("-" * 50)

    for query, latencies in search_results.items():
        print(
            f"{query:<15} "
            f"avg={statistics.mean(latencies):>7.3f} ms  "
            f"p50={statistics.median(latencies):>7.3f} ms  "
            f"p95={percentile(latencies, 95):>7.3f} ms"
        )


def run_benchmark(repository_path):
    repository_path = Path(
        repository_path
    ).resolve()

    if not repository_path.exists():
        raise ValueError(
            f"Repository does not exist: "
            f"{repository_path}"
        )

    if not repository_path.is_dir():
        raise ValueError(
            f"Path is not a directory: "
            f"{repository_path}"
        )

    print("\nCodePulse Benchmark")
    print("=" * 50)
    print(f"Repository: {repository_path}")

    lines_of_code = count_python_lines(
        repository_path
    )

    print("\nIndexing Performance")
    print("-" * 50)

    (
        service,
        indexed_files,
        indexing_times,
    ) = benchmark_indexing(repository_path)

    print("\nIndexing Summary")
    print("-" * 50)

    print(
        f"Indexed files:       "
        f"{indexed_files:,}"
    )
    print(
        f"Python LOC:          "
        f"{lines_of_code:,}"
    )
    print(
        f"Runs:                "
        f"{len(indexing_times)}"
    )
    print(
        f"Average:             "
        f"{statistics.mean(indexing_times):.3f} s"
    )
    print(
        f"P50:                 "
        f"{statistics.median(indexing_times):.3f} s"
    )
    print(
        f"Min:                 "
        f"{min(indexing_times):.3f} s"
    )
    print(
        f"Max:                 "
        f"{max(indexing_times):.3f} s"
    )

    search_results = benchmark_search(
        service
    )

    print_search_statistics(
        search_results
    )

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark CodePulse on a repository."
        )
    )

    parser.add_argument(
        "repository",
        help=(
            "Path to the repository "
            "to benchmark."
        ),
    )

    args = parser.parse_args()

    try:
        run_benchmark(args.repository)
    except ValueError as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()