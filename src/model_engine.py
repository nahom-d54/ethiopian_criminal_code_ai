import json
import faiss
from sentence_transformers import SentenceTransformer
from sqlalchemy.future import select
from .models import FaissMetadata  # Your SQLAlchemy model for metadata
from sqlalchemy.orm import Session


class FaissEngine:
    def __init__(
        self, index_file="criminal_code.index", metadata_file="faiss_metadata.json"
    ):
        self.index = faiss.read_index(index_file)
        self.metadata_file = metadata_file
        with open(metadata_file, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def query(self, question: str, top_k: int = 3):
        q_embedding = self.model.encode([question])
        D, I = self.index.search(q_embedding, top_k)
        return [self.metadata[i] for i in I[0]]


class FaissEnginePostgres:
    def __init__(self, db: Session, index_file="criminal_code.index"):
        self.db = db
        self.index = faiss.read_index(index_file)  # Reads the FAISS index file
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    async def query(self, question: str, top_k: int = 3):
        # Generate embedding for the query
        q_embedding = self.model.encode([question])

        # Perform search in the FAISS index to get the closest matches (IDs)
        D, INDEX = self.index.search(q_embedding, top_k)

        # Get the faiss_id for the closest matches
        faiss_ids = [
            int(i) for i in INDEX[0]
        ]  # FAISS returns indices, which we convert to faiss_id

        print(f"faiss_ids: {faiss_ids}")

        # Fetch the corresponding metadata from PostgreSQL using faiss_id
        result = await self.db.execute(
            select(FaissMetadata).where(FaissMetadata.id.in_(faiss_ids))
        )

        # Return the metadata results
        return result.scalars().all()
