
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.task import AITask
from app.schemas.planner import PlanRequest
from app.services.planner_service import generate_plan

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", status_code=201)
async def create_task(
    request: PlanRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await generate_plan(request.goal)

    task = AITask(
        goal=request.goal,
        plan=result.plan.model_dump(),
        model=result.model,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        latency_ms=result.latency_ms,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task

@router.get("")
async def list_tasks(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AITask)
        .order_by(AITask.created_at.desc())
        .limit(50)
    )
    return result.scalars().all()

@router.get("/{task_id}")
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(AITask, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task
