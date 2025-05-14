import json
import asyncio
from src.database import AsyncSessionLocal, engine, Base
from src.models import FaissMetadata
from sqlalchemy import select


async def migrate_metadata(json_file="faiss_metadata.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    async with AsyncSessionLocal() as db:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Check if any metadata already exists
        result = await db.execute(select(FaissMetadata.id))
        existing = result.scalars().first()
        if existing:
            print("Migration skipped: FAISS metadata already exists.")
            return

        # Otherwise, proceed to insert
        for item in metadata:
            entry = FaissMetadata(
                faiss_id=item["id"],
                title=item["title"],
                content=item["content"],
                book=item["book"],
                title_group=item["title_group"],
                chapter=item["chapter"],
            )
            db.add(entry)

        await db.commit()
        print("Migration complete.")


if __name__ == "__main__":
    asyncio.run(migrate_metadata())
