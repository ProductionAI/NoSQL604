import pymongo
import logging
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
uri = os.getenv("COSMOS_CONNECTION_STRING")


# Enable full wire protocol logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pymongo")
logger.setLevel(logging.DEBUG)

client = MongoClient(uri, retryWrites=False)
print(client.server_info())