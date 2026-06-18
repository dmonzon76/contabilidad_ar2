import http.cookiejar
import urllib.request
import urllib.parse
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
login_url = "http://127.0.0.1:8000/accounts/login/"
print("GET login page")
resp = opener.open(login_url + "?next=/dashboard/")
html = resp.read().decode("utf-8", errors="ignore")
print("GET login status", resp.status)
print(
    "Cookies after GET",
    [(c.name, c.value, c.domain, c.path, c.secure, c.expires) for c in cj],
)
print("---")

m = re.search(
    r"name=[\"\']csrfmiddlewaretoken[\"\'] value=[\"\']([^\"\']+)[\"\']", html
)
print("csrf token found", bool(m), m.group(1) if m else None)
if not m:
    raise RuntimeError("No CSRF token found")

print("--- POST login ---")
post_data = urllib.parse.urlencode(
    {
        "username": "daniel",
        "password": "django123",
        "next": "/dashboard/",
        "csrfmiddlewaretoken": m.group(1),
    }
).encode()
req = urllib.request.Request(
    login_url,
    data=post_data,
    headers={
        "Referer": login_url + "?next=/dashboard/",
        "Content-Type": "application/x-www-form-urlencoded",
    },
)
try:
    resp = opener.open(req)
    print("Login POST status", resp.status)
    print(
        "Headers",
        [
            (k, v)
            for k, v in resp.getheaders()
            if k.lower() in ("set-cookie", "location")
        ],
    )
    print(
        "Cookies after POST",
        [(c.name, c.value, c.domain, c.path, c.secure, c.expires) for c in cj],
    )
    print("Final URL", resp.geturl())
    body = resp.read(300).decode("utf-8", errors="ignore")
    print("Body snippet", body.replace("\n", " "))
except urllib.error.HTTPError as e:
    print("Login POST failed", e.code)
    print(
        "Headers",
        [
            (k, v)
            for k, v in e.headers.items()
            if k.lower() in ("set-cookie", "location")
        ],
    )
    print(
        "Cookies after failed POST",
        [(c.name, c.value, c.domain, c.path, c.secure, c.expires) for c in cj],
    )
    raise

print("--- GET dashboard ---")
resp = opener.open("http://127.0.0.1:8000/dashboard/")
print("GET dashboard status", resp.status)
print("Dashboard URL", resp.geturl())
print(
    "Cookies for dashboard",
    [(c.name, c.value, c.domain, c.path, c.secure, c.expires) for c in cj],
)
print(
    "Body snippet", resp.read(300).decode("utf-8", errors="ignore").replace("\n", " ")
)
