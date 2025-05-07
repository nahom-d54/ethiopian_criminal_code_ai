from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from src.model_engine import FaissEngine, FaissEnginePostgres
from pydantic import BaseModel
from src.auth import verify_api_key
from src.admin_routes import router as admin_router
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the FAISS Engine once when the app starts
    app.state.faiss_slow_engine = FaissEngine()
    db_generator = get_db()
    db = await anext(db_generator)  # Python 3.10+  # noqa: F821
    app.state.faiss_fast_engine = FaissEnginePostgres(db=db)
    yield
    # Clean up resources when the app shuts down
    app.state.faiss_slow_engine = None
    app.state.faiss_fast_engine = None


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    prompt: str
    top_k: int = 3


@app.post("/v1/chat/completions")
async def chat(req: ChatRequest, api_key=Depends(verify_api_key)):
    engine = app.state.faiss_slow_engine
    if not engine:
        return HTTPException(status_code=503, detail="FAISS engine not initialized")
    max_top_k = 10

    if req.top_k > max_top_k:
        return {"error": f"top_k cannot be greater than {max_top_k}"}

    result = engine.query(req.prompt, req.top_k)
    return {"results": result}


@app.post("/v1/chat/fast/completions")
async def fast_chat(req: ChatRequest, api_key=Depends(verify_api_key)):
    engine = app.state.faiss_fast_engine

    if not engine:
        return HTTPException(status_code=503, detail="FAISS engine not initialized")
    max_top_k = 10

    if req.top_k > max_top_k:
        return {"error": f"top_k cannot be greater than {max_top_k}"}
    result = await engine.query(req.prompt, req.top_k)
    return {"results": result}


app.include_router(admin_router)
