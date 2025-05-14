from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from pydantic import BaseModel
from src.database import Base


class AdminUser(Base):
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superadmin = Column(Boolean, default=False, nullable=False)


class APIKey(Base):
    key = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)


class UsageLog(Base):
    api_key_id = Column(Integer, ForeignKey("apikey.id"))
    endpoint = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class FaissMetadata(Base):
    faiss_id = Column(String, unique=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    book = Column(String, nullable=False)
    title_group = Column(String, nullable=False)
    chapter = Column(String, nullable=True)


# pydantic model
class ChatRequest(BaseModel):
    prompt: str
    top_k: int = 3
