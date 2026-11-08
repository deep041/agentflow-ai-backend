from pydantic import BaseModel, Field

class AgentRequest(BaseModel):
    message: str = Field(min_length=3, max_length=2000)

class ToolExecution(BaseModel):
    tool: str
    arguments: dict
    result: object

class AgentResponse(BaseModel):
    answer: str
    steps: list[ToolExecution]
    iterations: int
