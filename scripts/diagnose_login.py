import re
import requests

session = requests.Session()
login_url = "http://127.0.0.1:8000/accounts/login/"
resp = session.get(login_url + "?next=/dashboard/")
print("GET status", resp.status_code)
print("Cookies after GET", session.cookies.get_dict())
html = resp.text
m = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', html)
print("CSRF token found", bool(m), m.group(1) if m else None)

post_data = {
    "username": "daniel",
    "password": "django123",
    "next": "/dashboard/",
    "csrfmiddlewaretoken": m.group(1),
}
resp = session.post(
    login_url, data=post_data, headers={"Referer": login_url + "?next=/dashboard/"}
)
print("POST status", resp.status_code)
print("POST URL", resp.url)
print("Response cookies", session.cookies.get_dict())
print(
    "Response headers",
    {k: v for k, v in resp.headers.items() if k.lower() in ("set-cookie", "location")},
)
print("Text snippet", resp.text[:300].replace("\n", " "))
resp2 = session.get("http://127.0.0.1:8000/dashboard/")
print("Dashboard status", resp2.status_code)
print("Dashboard URL", resp2.url)
print("Final cookies", session.cookies.get_dict())
print("Dashboard snippet", resp2.text[:300].replace("\n", " "))
