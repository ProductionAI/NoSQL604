import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("COSMOS_CONNECTION_STRING")

print(uri)

#client = MongoClient(uri)
client = MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=False,
    retryWrites=False,          # Cosmos doesn't support retryWrites
    serverSelectionTimeoutMS=30000,
    socketTimeoutMS=30000,
)

db = client["myDatabase"]
col = db["myCollection"]

print("✅ Connected to Cosmos DB")

test_col = db["testWrite"]
test_col.insert_one({"test": True})
print("Write succeeded")

'''
# INSERT
result = col.insert_many([
    {"name": "Alice", "age": 30, "city": "Seattle"},
    {"name": "Bob",   "age": 25, "city": "Austin"},
    {"name": "Carol", "age": 35, "city": "Seattle"},
])
print(f"Inserted {len(result.inserted_ids)} docs")

# Always close the client when done
client.close()
'''