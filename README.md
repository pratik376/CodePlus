# CodePulse

CodePulse is a code search and repository analysis engine built in Python.

It indexes source-code repositories, ranks relevant files for search queries, analyzes dependencies between Python modules, and estimates which files may be affected when a dependency changes.

The core search and analysis logic is implemented directly rather than relying on an external search engine. CodePulse currently combines an **inverted index, BM25 ranking, heap-based Top-K retrieval, Python AST parsing, and graph algorithms**, and exposes the functionality through a **FastAPI REST API**.

---

## What CodePulse Does

### Repository Search

CodePulse recursively scans a source-code repository and indexes supported source files.

Instead of scanning every file whenever a user searches, it builds an **inverted index**:

```text
token
    -> auth.py: 4
    -> middleware.py: 2

database
    -> database.py: 6
    -> user.py: 1
```

Each term points to the documents containing it and stores its frequency within each document.

When a query is submitted, CodePulse:

```text
Search Query
     |
     v
 Tokenization
     |
     v
Inverted Index
     |
     v
Candidate Files
     |
     v
 BM25 Ranking
     |
     v
Top-K Selection
     |
     v
Ranked Results
```

This avoids repeatedly scanning the entire repository at query time.

---

### BM25 Ranking

Matching a query does not necessarily mean every matching file is equally relevant.

CodePulse uses **BM25** to rank candidate source files based on:

- Term frequency
- Document frequency
- Document length
- Average document length
- Term rarity

For example:

```text
Query: authentication token

1. auth.py          score=5.128
2. middleware.py    score=3.795
3. user.py          score=2.866
```

Only files containing at least one query term are considered for ranking.

---

### Top-K Retrieval

After BM25 scores candidate files, CodePulse uses a **heap-based Top-K selection** to return the highest-scoring results.

```text
Candidate Files
      |
      v
  BM25 Scores
      |
      v
 Top-K Heap
      |
      v
Best Results
```

This avoids requiring a complete sort when only a small number of results are requested.

---

## Repository Dependency Analysis

CodePulse also performs static analysis on Python repositories.

Python source files are parsed using the built-in **Abstract Syntax Tree (AST)** module to identify imports between internal modules.

For example:

```text
api.py
  |
  v
auth.py
  |
  v
database.py
```

This is represented internally as a **directed dependency graph**.

---

### Dependency Analysis

CodePulse can find both direct and transitive dependencies.

For example:

```text
api.py
  |
  +--> auth.py
          |
          +--> database.py
```

If `api.py` depends on `auth.py`, and `auth.py` depends on `database.py`, CodePulse can determine that `database.py` is also a transitive dependency of `api.py`.

---

### Impact Analysis

CodePulse maintains a reverse dependency graph to determine which files may be affected when another file changes.

For example:

```text
database.py
     ^
     |
   auth.py
     ^
     |
   api.py
```

If `database.py` changes, CodePulse can identify `auth.py` and `api.py` as potentially impacted files.

Impact results are separated into:

```text
PRODUCTION IMPACT
----------------------------------------
app/search/index.py
app/search/bm25.py
app/search/engine.py

AFFECTED TESTS
----------------------------------------
app/tests/test_index.py
app/tests/test_bm25.py
```

This makes the analysis more useful when deciding which application components and tests may need attention after a change.

---

### Circular Dependency Detection

CodePulse uses graph traversal to detect circular dependencies.

Example:

```text
a.py --> b.py --> c.py
 ^                 |
 |_________________|
```

Circular dependencies can indicate tight coupling between modules and make a codebase more difficult to maintain.

---

## Architecture

```text
                  Repository
                      |
                      v
              Repository Loader
                      |
            +---------+---------+
            |                   |
            v                   v
      Search Engine         AST Parser
            |                   |
            v                   v
     Inverted Index      Dependency Graph
            |                   |
            v             +-----+-----+
          BM25            |           |
            |             v           v
            v       Dependencies    Impact
          Top-K            |           |
            |              |           |
            +--------------+-----------+
                           |
                           v
                    Repository Service
                           |
                           v
                        FastAPI
```

The API layer is kept separate from the search and dependency-analysis logic so that the core algorithms can be tested independently.

---

## Techniques and Data Structures

### Inverted Index

CodePulse stores:

```text
term -> {document: frequency}
```

This allows candidate files to be retrieved directly for a query term instead of scanning every source file.

### Hash Maps

Python dictionaries are used extensively for:

- Posting lists
- Document metadata
- Term frequencies
- Dependency mappings
- Reverse dependency mappings

### Sets

Sets are used for:

- Candidate-document collection
- Duplicate prevention
- Graph traversal
- Visited-node tracking

### Heap

Python's heap-based utilities are used for **Top-K search retrieval**.

### Directed Graphs

Repository dependencies are represented as directed graphs.

The graph supports:

- Direct dependency lookup
- Transitive dependency traversal
- Reverse dependency traversal
- Change-impact analysis
- Cycle detection

### Breadth-First Search

BFS is used to traverse dependency relationships and determine transitive impact through the reverse dependency graph.

### Depth-First Search

DFS with a recursion stack is used for circular-dependency detection.

### Python AST

Python's `ast` module is used to parse source files and identify import relationships structurally instead of relying on regular expressions.

### BM25

BM25 provides relevance ranking using term frequency, document frequency, document-length normalization, and term rarity.

---

## Project Structure

```text
CodePlus/
│
├── app/
│   ├── repository/
│   │   └── loader.py
│   │
│   ├── schemas/
│   │   └── search.py
│   │
│   ├── search/
│   │   ├── tokenizer.py
│   │   ├── index.py
│   │   ├── bm25.py
│   │   └── engine.py
│   │
│   ├── services/
│   │   └── repository_service.py
│   │
│   └── tests/
│       ├── test_api.py
│       ├── test_bm25.py
│       ├── test_graph.py
│       ├── test_index.py
│       ├── test_loader.py
│       └── test_tokenizer.py
│
├── graph/
│   ├── dependency_graph.py
│   └── parser.py
│
├── analyze.py
├── demo.py
├── main.py
├── requirements.txt
└── README.md
```

---

## REST API

CodePulse exposes the search and repository-analysis engine through **FastAPI**.

Current endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check service status and indexed file count |
| `POST` | `/repositories/index` | Index a local source-code repository |
| `POST` | `/search` | Search indexed source files |
| `GET` | `/dependencies` | Find transitive dependencies of a file |
| `GET` | `/impact` | Find files potentially affected by a change |
| `GET` | `/cycles` | Check the repository for dependency cycles |

FastAPI automatically provides interactive OpenAPI documentation through Swagger UI.

---

## Running CodePulse

### 1. Clone the Repository

```bash
git clone https://github.com/pratik376/CodePlus.git
cd CodePlus
```

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Tests

```bash
python -m pytest -v
```

The test suite covers the search engine, repository loader, BM25 ranking, dependency graph, impact analysis, cycle detection, and REST API behavior.

### 5. Start the API

```bash
python -m uvicorn main:app --reload
```

The server will start at:

```text
http://127.0.0.1:8000
```

### 6. Open Swagger

Navigate to:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing all CodePulse endpoints.

---

## Example Usage

### Index a Repository

Use:

```text
POST /repositories/index
```

Example request:

```json
{
  "path": "D:\\Projects\\my-project"
}
```

---

### Search Source Code

Use:

```text
POST /search
```

Example request:

```json
{
  "query": "authentication token",
  "limit": 5
}
```

Example response:

```json
[
  {
    "file": "src/auth.py",
    "score": 5.128
  },
  {
    "file": "src/user.py",
    "score": 2.866
  }
]
```

---

### Analyze Dependencies

Use:

```text
GET /dependencies?file=app/search/engine.py
```

CodePulse returns the transitive internal dependencies of that file.

---

### Analyze Change Impact

Use:

```text
GET /impact?file=app/search/tokenizer.py
```

Example response:

```json
{
  "file": "app/search/tokenizer.py",
  "production_files": [
    "app/search/index.py",
    "app/search/bm25.py",
    "app/search/engine.py"
  ],
  "test_files": [
    "app/tests/test_index.py",
    "app/tests/test_bm25.py",
    "app/tests/test_tokenizer.py"
  ]
}
```

---

### Detect Circular Dependencies

Use:

```text
GET /cycles
```

Example response:

```json
{
  "has_cycle": false
}
```

---

## Testing

The current implementation includes automated tests for:

- Inverted-index insertion, removal, and updates
- BM25 relevance ranking
- Top-K result limits
- Tokenization
- Repository loading
- Ignored directory handling
- Dependency traversal
- Reverse impact analysis
- Circular dependency detection
- Python dependency parsing
- FastAPI endpoints
- API error handling

Run all tests with:

```bash
python -m pytest -v
```

---

## Technology Stack

**Language**

- Python

**Backend**

- FastAPI
- Uvicorn
- Pydantic

**Search and Algorithms**

- Inverted Index
- BM25
- Heap-based Top-K retrieval
- Directed Graphs
- BFS
- DFS
- Python AST

**Testing**

- pytest
- FastAPI TestClient