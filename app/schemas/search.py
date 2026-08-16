from pydantic import BaseModel, Field


class RepositoryRequest(BaseModel):
    path: str


class SearchResponse(BaseModel):
    file: str
    score: float


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=500,
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )