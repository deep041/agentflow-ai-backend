from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.planner import router as planner_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.research import router as research_router
from app.api.routes.agent import router as agent_router

app = FastAPI(
    title="AgentFlow AI API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(planner_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(research_router, prefix="/api/v1")
app.include_router(agent_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "healthy"}