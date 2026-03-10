import chromadb
from chromadb.config import Settings

# 1. Connect to the Docker container
# Replace 'localhost' with the IP if running on a different machine
client = chromadb.HttpClient(host='localhost', port=8000)

# 2. Get or Create a collection
# Using 'get_or_create' prevents errors if the script runs twice
collection = client.get_or_create_collection(name="docker_knowledge_base")

# 3. Add data (The process remains the same)
collection.add(
    documents=[
        "Docker is a platform for developing, shipping, and running applications.",
        "Kubernetes is an open-source system for automating deployment of containers.",
        "Microservices architecture breaks apps into small, independent services."
    ],
    metadatas=[{"type": "devops"}, {"type": "devops"}, {"type": "arch"}],
    ids=["doc1", "doc2", "doc3"]
)

# 4. Query the remote database
query_text = "How do I manage containerized apps at scale?"
results = collection.query(
    query_texts=[query_text],
    n_results=1
)

print(f"Query: {query_text}")
print(f"Top Result: {results['documents'][0][0]}")