
from pydantic import BaseModel, Field, HttpUrl


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=10,
        max_length=2000
    )


class ResearchSource(BaseModel):
    title: str
    url: str


class ResearchResponse(BaseModel):
    query: str
    report: str
    sources: list[ResearchSource]
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
