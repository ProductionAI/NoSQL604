from urllib.parse import urlparse, unquote
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("COSMOS_CONNECTION_STRING")
parsed = urlparse(uri)

raw_key = parsed.password
decoded_key = unquote(raw_key)

print("Raw key length:    ", len(raw_key))
print("Decoded key length:", len(decoded_key))
print("Contains + :", "+" in raw_key)
print("Contains / :", "/" in raw_key)
print("Contains % :", "%" in raw_key)
print("Keys match:", raw_key == decoded_key)