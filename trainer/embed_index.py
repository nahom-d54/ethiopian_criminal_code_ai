import json
import faiss
from sentence_transformers import SentenceTransformer


# Function to index documents and create FAISS index
def index_corpus(corpus_file, index_file, metadata_file):
    # Load the structured articles
    with open(corpus_file, "r", encoding="utf-8") as f:
        docs = json.load(f)

    # Use a SentenceTransformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Convert texts to embeddings
    texts = [doc["content"] for doc in docs]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Build the FAISS index
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Optional: Save the index for later use
    faiss.write_index(index, index_file)

    # Save metadata so we can retrieve it by index
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False)

    print(
        f"Indexing complete. FAISS index saved to {index_file} and metadata saved to {metadata_file}"
    )


# Example usage
if __name__ == "__main__":
    index_corpus(
        "C:\\Users\\nahom\\Desktop\\assignment\\faiss_api\\trainer\\corpus-v2-out.json",
        "criminal_code_v2.index",
        "faiss_metadata_v2.json",
    )
