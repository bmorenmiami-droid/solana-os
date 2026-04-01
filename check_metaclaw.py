import urllib.request
try:
    r = urllib.request.urlopen('http://localhost:30000/healthz', timeout=5)
    print(f"Status: {r.status}")
    print(f"Body: {r.read()}")
except Exception as e:
    print(f"Error: {e}")
