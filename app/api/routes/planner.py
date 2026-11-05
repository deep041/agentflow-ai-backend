from fastapi import APIRouter

from app.schemas.planner import PlanRequest, TaskPlan
from app.services.planner_service import generate_plan

router = APIRouter(prefix="/planner", tags=["Planner"])

@router.post("/generate", response_model=TaskPlan)
async def create_plan(request: PlanRequest):
    return await generate_plan(request.goal)