
import logging

from fastapi import APIRouter, HTTPException
from openai import OpenAIError

from app.agents.researcher import research_topic
from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)

router = APIRouter(
    prefix="/research",
    tags=["Research Agent"],
)

logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=ResearchResponse,
)
async def create_research(
    request: ResearchRequest,
):
    try:
        return await research_topic(request.query)

    except OpenAIError:
        logger.exception("Research agent API failure")
        raise HTTPException(
            status_code=502,
            detail="Research service unavailable",
        )
