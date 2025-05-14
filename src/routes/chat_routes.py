from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from src.models import ChatRequest
from src.auth import verify_api_key
from src import config


chat_router = APIRouter(prefix="/chat")


@chat_router.post("/completions")
async def chat(req: ChatRequest, request: Request, api_key=Depends(verify_api_key)):
    engine = request.app.state.faiss_engine
    if not engine:
        return HTTPException(status_code=503, detail="FAISS engine not initialized")
    max_top_k = getattr(config, "max_top_k", 3)

    if req.top_k > max_top_k:
        return {"error": f"top_k cannot be greater than {max_top_k}"}

    result = engine.query(req.prompt, req.top_k)
    return {"results": result}
