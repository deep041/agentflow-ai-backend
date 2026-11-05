from typing import Literal
from pydantic import BaseModel, Field

class PlanRequest(BaseModel):
    goal: str = Field(min_length=10, max_length=2000)

class PlanStep(BaseModel):
    title: str
    description: str
    agent: Literal["researcher", "analyst", "writer"]
    estimated_minutes: int = Field(ge=1, le=240)

class TaskPlan(BaseModel):
    title: str
    summary: str
    steps: list[PlanStep] = Field(min_length=1, max_length=8)