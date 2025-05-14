from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.model_engine import FaissEngine
from src.routes.api_route import api_route
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the FAISS Engine once when the app starts
    app.state.faiss_engine = FaissEngine()
    yield
    # Clean up resources when the app shuts down
    app.state.faiss_engine = None


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use with caution in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_route)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port="8080")
