from fastapi import FastAPI, HTTPException

from app.schemas.search import (
    DependencyResponse,
    ImpactResponse,
    RepositoryRequest,
    RepositoryResponse,
    SearchRequest,
    SearchResultResponse,
)
from app.services.repository_service import (
    RepositoryService,
)


app = FastAPI(
    title="CodePulse",
    description=(
        "Code search and repository "
        "intelligence platform"
    ),
    version="0.1.0",
)


service = RepositoryService()

@app.get("/")
def root():
    return {
        "name": "CodePulse",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "indexed_files": (
            service
            .search_engine
            .index
            .document_count
        ),
    }


@app.post(
    "/repositories/index",
    response_model=RepositoryResponse,
)
def index_repository(
    request: RepositoryRequest,
):
    try:
        count = service.index_repository(
            request.path
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except NotADirectoryError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return RepositoryResponse(
        indexed_files=count
    )


@app.post(
    "/search",
    response_model=list[SearchResultResponse],
)
def search(
    request: SearchRequest,
):
    results = service.search(
        query=request.query,
        limit=request.limit,
    )

    return [
        SearchResultResponse(
            file=result.doc_id,
            score=round(
                result.score,
                4,
            ),
        )
        for result in results
    ]


@app.get(
    "/dependencies",
    response_model=DependencyResponse,
)
def dependencies(file: str):
    try:
        result = service.dependencies(file)

    except RuntimeError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )

    return DependencyResponse(
        file=file,
        dependencies=result,
    )


@app.get(
    "/impact",
    response_model=ImpactResponse,
)
def impact(file: str):
    try:
        production_files, test_files = (
            service.impact(file)
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )

    return ImpactResponse(
        file=file,
        production_files=production_files,
        test_files=test_files,
    )


@app.get("/cycles")
def cycles():
    try:
        has_cycle = service.has_cycle()

    except RuntimeError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )

    return {
        "has_cycle": has_cycle
    }