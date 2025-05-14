from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import APIKey, UsageLog, AdminUser
from src.database import get_db
from src.auth import (
    get_current_admin,
    get_password_hash,
    create_access_token,
    verify_password,
)
import secrets


router = APIRouter(prefix="/admin")


@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AdminUser).where(AdminUser.username == username))
    admin = result.scalar_one_or_none()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": admin.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/users/create")
async def create_admin_user(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    if not current_admin.is_superadmin:
        raise HTTPException(status_code=403, detail="Not authorized")

    hashed_pw = get_password_hash(password)
    user = AdminUser(username=username, hashed_password=hashed_pw)
    db.add(user)
    await db.commit()
    return {"message": "Admin user created"}


@router.post("/keys/create")
async def create_key(
    owner: str,
    db: AsyncSession = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    key = secrets.token_hex(16)
    api_key = APIKey(key=key, owner=owner)
    db.add(api_key)
    await db.commit()
    return {"key": key}


@router.post("/keys/deactivate")
async def deactivate_key(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(APIKey).where(APIKey.key == key))
    api_key = result.scalar_one_or_none()
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")
    api_key.active = False
    await db.commit()
    return {"message": "API key deactivated"}


@router.get("/keys")
async def list_keys(
    db: AsyncSession = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(APIKey))
    return result.scalars().all()


@router.get("/usage")
async def usage(
    db: AsyncSession = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(UsageLog))
    return result.scalars().all()
