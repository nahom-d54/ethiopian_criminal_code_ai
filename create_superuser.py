import asyncio
from getpass import getpass
from sqlalchemy.future import select
from src.database import AsyncSessionLocal, engine, Base
from src.models import AdminUser
from src.auth import get_password_hash
import argparse


async def create_superuser(username=None, password=None, email=None):
    if not username:
        username = input("Username: ").strip()
    if not password:
        password = getpass("Password: ")
        password2 = getpass("Confirm Password: ")
        if password != password2:
            print("Passwords do not match.")
            return
    if not email:
        email = input("Email: ").strip()

    hashed_password = get_password_hash(password)

    async with AsyncSessionLocal() as db:
        # Create tables if they don't exist
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Check if user exists
        result = await db.execute(
            select(AdminUser).where(
                AdminUser.username == username or AdminUser.email == email
            )
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            print("A user with that username or email already exists.")
            return

        # Create the user
        user = AdminUser(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_superadmin=True,
        )
        db.add(user)
        await db.commit()
        print(f"Superuser '{username}' created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a superuser admin account.")
    parser.add_argument("-u", "--username", type=str, help="Username of the admin")
    parser.add_argument("-p", "--password", type=str, help="Password of the admin")
    parser.add_argument("-e", "--email", type=str, help="Email of the admin")
    args = parser.parse_args()
    asyncio.run(create_superuser(args.username, args.password, args.email))
