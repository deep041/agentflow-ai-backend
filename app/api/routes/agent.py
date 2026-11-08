
import logging

from fastapi import APIRouter, HTTPException
from openai import OpenAIError

from app.agents.tool_agent import run_agent
from app.schemas.agent import AgentRequest, AgentResponse

router = APIRouter(
    prefix="/agent",
    tags=["Tool Agent"],
)

logger = logging.getLogger(__name__)

@router.post("/run", response_model=AgentResponse)
async def execute_agent(request: AgentRequest):
    try:
        return await run_agent(request.message)

    except OpenAIError:
        logger.exception("Agent model request failed")
        raise HTTPException(
            status_code=502,
            detail="AI service unavailable",
        )
