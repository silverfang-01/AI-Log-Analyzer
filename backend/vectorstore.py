import chromadb, uuid
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.PersistentClient(path=".chromadb")
collection = chroma_client.get_or_create_collection(name="logs")
model = SentenceTransformer("all-MiniLM-L6-v2")

def add_logs_to_vectorstore(log_df):
    texts = log_df["full"].tolist()           # <— use full line
    embeddings = model.encode(texts).tolist()
    ids = [str(uuid.uuid4()) for _ in texts]
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=log_df.drop(columns=["full"]).to_dict(orient="records"),
        ids=ids,
    )

def search_logs(query, k=5):
    vec = model.encode([query]).tolist()
    return collection.query(query_embeddings=vec, n_results=k)
