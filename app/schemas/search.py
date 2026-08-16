from pydantic import BaseModel, Field


class RepositoryRequest(BaseModel):
    path: str = Field(min_length=1)


class RepositoryResponse(BaseModel):
    indexed_files: int


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=100)


class SearchResultResponse(BaseModel):
    file: str
    score: float


class DependencyResponse(BaseModel):
    file: str
    dependencies: list[str]


class ImpactResponse(BaseModel):
    file: str
    production_files: list[str]
    test_files: list[str]