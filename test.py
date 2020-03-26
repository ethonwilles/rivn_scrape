import requests
import json

payload = {
    "has_priv" : True,
 "priv_url" : "https://iamaurl.org",
  "url" : "snapchat.com"
  }

r = requests.post("http://localhost:5000/audit-results-post", json=payload)

print(r.json())