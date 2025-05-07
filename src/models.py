from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from .database import Base


class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superadmin = Column(Boolean, default=False, nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())


class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())


class UsageLog(Base):
    __tablename__ = "usage_logs"
    id = Column(Integer, primary_key=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    endpoint = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class FaissMetadata(Base):
    __tablename__ = "faiss_metadata"
    id = Column(Integer, primary_key=True)
    faiss_id = Column(String, unique=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    book = Column(String, nullable=False)
    title_group = Column(String, nullable=False)
    chapter = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
