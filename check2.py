from pymongo import MongoClient
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("COSMOS_CONNECTION_STRING")
parsed = urlparse(uri)

print("=== URI CHECK ===")
print("Scheme:", parsed.scheme)
print("Host:", parsed.hostname)
print("Port:", parsed.port)
print("Username:", parsed.username)
print("Key length:", len(parsed.password))
print("Query string:", parsed.query)
print()

client = MongoClient(uri, retryWrites=False, serverSelectionTimeoutMS=5000)

print("=== SERVER INFO ===")
print(client.server_info())
