import pytest
from pydantic import ValidationError

from app.schemas.planner import PlanRequest, TaskPlan

def test_valid_goal():
    request = PlanRequest(
        goal="Research AI tools and create a report"
    )
    assert request.goal.startswith("Research")

def test_short_goal_rejected():
    with pytest.raises(ValidationError):
        PlanRequest(goal="Hi")

def test_invalid_agent_rejected():
    with pytest.raises(ValidationError):
        TaskPlan(
            title="Research",
            summary="Compare tools",
            steps=[{
                "title": "Collect data",
                "description": "Research products",
                "agent": "unknown",
                "estimated_minutes": 20,
            }],
        )