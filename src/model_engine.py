import json
import faiss
from sentence_transformers import SentenceTransformer


class FaissEngine:
    def __init__(
        self,
        index_file="criminal_code_v2.index",
        metadata_file="faiss_metadata_v2.json",
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
