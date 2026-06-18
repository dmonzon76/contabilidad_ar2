import http.client
import urllib.parse
import re

conn = http.client.HTTPConnection("127.0.0.1", 8000)
conn.request("GET", "/accounts/login/?next=/dashboard/")
resp = conn.getresponse()
html = resp.read().decode("utf-8", errors="ignore")
print("GET status", resp.status)
print("GET headers", resp.getheaders())
set_cookie = [h for h in resp.getheaders() if h[0].lower() == "set-cookie"]
print("GET set-cookie", set_cookie)
csrftoken = None
for h in resp.getheaders():
    if h[0].lower() == "set-cookie" and "csrftoken=" in h[1]:
        m = re.search(r"csrftoken=([^;]+)", h[1])
        if m:
            csrftoken = m.group(1)
print("csrftoken", csrftoken)

m = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', html)
print("csrf token found", bool(m), m.group(1) if m else None)
if not m:
    raise SystemExit("csrf token not found")

auth = urllib.parse.urlencode(
    {
        "username": "daniel",
        "password": "django123",
        "next": "/dashboard/",
        "csrfmiddlewaretoken": m.group(1),
    }
)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": f"csrftoken={csrftoken}" if csrftoken else "",
    "Referer": "http://127.0.0.1:8000/accounts/login/?next=/dashboard/",
}
conn.request("POST", "/accounts/login/", auth, headers)
resp = conn.getresponse()
print("POST status", resp.status)
print("POST headers", resp.getheaders())
post_set_cookie = [h for h in resp.getheaders() if h[0].lower() == "set-cookie"]
print("POST set-cookie", post_set_cookie)
print("POST location", resp.getheader("location"))
body = resp.read().decode("utf-8", errors="ignore")
print("body snippet", body[:200].replace("\n", " "))
