from datetime import datetime, timezone
import urllib.request

# Your local UTC time
print("Local UTC:", datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"))

# Azure's actual time (from their servers)
req = urllib.request.urlopen("https://portal.azure.com")
print("Azure time:", req.headers.get("Date"))