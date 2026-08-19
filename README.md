# CodePulse

CodePulse is a Python repository search and analysis engine. It combines **BM25 code search** with **AST-based dependency analysis** to search source files, trace dependencies, estimate change impact, and detect circular dependencies.

The search and graph logic is implemented from scratch and exposed through a **FastAPI REST API**.

## Highlights

* Inverted index + BM25 ranking with heap-based Top-K retrieval
* Python AST-based dependency graph
* Transitive dependency and change-impact analysis
* Circular dependency detection
* FastAPI REST API
* **20 automated tests** with GitHub Actions CI

## Performance

Benchmarked on the open-source FastAPI repository:

| Metric               |       Result |
| -------------------- | -----------: |
| Python files indexed |    **1,142** |
| Python LOC           |  **112,998** |
| Median indexing time |  **1.946 s** |
| Search operations    |      **500** |
| P95 search latency   | **1.016 ms** |

Indexing was measured across 5 runs. Search latency was measured across 5 queries with 100 runs per query. Results are machine-dependent.

The benchmark can be reproduced with `benchmarks/benchmark.py`.

## Architecture

```text
Repository
    |
    +----> Repository Loader ----> Inverted Index ----> BM25 ----> Top-K
    |
    +----> AST Parser -----------> Dependency Graph
                                      |        |
                                Dependencies  Impact
                                      \        /
                                   Repository Service
                                          |
                                       FastAPI
```

## API

| Method | Endpoint              | Purpose                      |
| ------ | --------------------- | ---------------------------- |
| `POST` | `/repositories/index` | Index a repository           |
| `POST` | `/search`             | Search source files          |
| `GET`  | `/dependencies`       | Find transitive dependencies |
| `GET`  | `/impact`             | Analyze change impact        |
| `GET`  | `/cycles`             | Detect dependency cycles     |
| `GET`  | `/health`             | Check service status         |

Interactive API documentation is available at `/docs` when the server is running.

## Run Locally

```bash
git clone https://github.com/pratik376/CodePlus.git
cd CodePlus

python -m venv .venv
python -m pip install -r requirements.txt

python -m pytest -v
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Benchmark Another Repository

```bash
python benchmarks/benchmark.py /path/to/repository
```

## Tech

**Python · FastAPI · Pydantic · pytest · GitHub Actions · BM25 · Inverted Index · Python AST · Graph Algorithms**
