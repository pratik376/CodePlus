from fastapi import FastAPI, HTTPException

from graph.parser import PythonDependencyParser
from app.repository.loader import RepositoryLoader
from app.schemas.search import (
    RepositoryRequest,
    SearchRequest,
    SearchResponse,
)
from app.search.engine import SearchEngine


app = FastAPI(
    title="CodePulse",
    description=(
        "Code search and repository "
        "intelligence platform"
    ),
    version="0.1.0",
)


search_engine = SearchEngine()
repository_loader = RepositoryLoader(
    search_engine
)

dependency_graph = None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "documents": (
            search_engine
            .index
            .document_count
        ),
    }


@app.post("/repositories/index")
def index_repository(
    request: RepositoryRequest,
):
    global dependency_graph

    try:
        count = repository_loader.load(
            request.path
        )

        parser = PythonDependencyParser()

        dependency_graph = (
            parser.parse_repository(
                request.path
            )
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    return {
        "indexed_files": count,
    }


@app.post(
    "/search",
    response_model=list[SearchResponse],
)
def search(request: SearchRequest):
    results = search_engine.search(
        query=request.query,
        limit=request.limit,
    )

    return [
        SearchResponse(
            file=result.doc_id,
            score=round(
                result.score,
                4,
            ),
        )
        for result in results
    ]


@app.get("/dependencies")
def dependencies(file: str):
    if dependency_graph is None:
        raise HTTPException(
            status_code=400,
            detail="No repository indexed",
        )

    return {
        "file": file,
        "dependencies": (
            dependency_graph
            .transitive_dependencies(file)
        ),
    }


@app.get("/impact")
def impact(file: str):
    if dependency_graph is None:
        raise HTTPException(
            status_code=400,
            detail="No repository indexed",
        )

    return {
        "file": file,
        "impacted_files": (
            dependency_graph
            .impact_analysis(file)
        ),
    }