import json
import re
from typing import Optional

from bs4 import BeautifulSoup

from ._session import _Session, BASE_URL
from .exceptions import AuthError


def _extract_json_object(text: str, after_pattern: str) -> Optional[dict]:
    """Extract the first JSON object found after `after_pattern` in `text`."""
    m = re.search(after_pattern, text)
    if not m:
        return None
    i = m.end()
    while i < len(text) and text[i] in " \t\n\r":
        i += 1
    if i >= len(text) or text[i] != "{":
        return None
    depth = 0
    in_string = False
    escape = False
    start = i
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    return None


def login(session: _Session, identifier: str, token: str, use_puk: bool) -> None:
    path = "/de/customer/login/puk" if use_puk else "/de/customer/login/account"
    r = session.http.post(
        BASE_URL + path,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "X-Requested-With": "XMLHttpRequest",
            "X-AUTH-SELF-CARE": "1",
        },
        json={"identifier": identifier, "token": token},
    )
    if not r.ok:
        raise AuthError(f"Login failed: HTTP {r.status_code}")


def init_session(session: _Session) -> None:
    r = session.http.get(BASE_URL + "/customer/dashboard/")
    if not r.ok:
        raise AuthError(f"Failed to fetch dashboard: HTTP {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")
    meta = soup.find("meta", {"name": "csrf-token"})
    if not meta or not meta.get("content"):
        raise AuthError("CSRF token not found in dashboard response")
    session.csrf_token = meta["content"]

    all_scripts = "".join(s.string for s in soup.find_all("script") if s.string)
    user_data = _extract_json_object(all_scripts, r"'user'\s*:\s*")
    if not user_data:
        raise AuthError("Could not find user data in dashboard")

    session.user_id = user_data["id"]
    accounts = user_data.get("accounts", [])
    if not accounts or not accounts[0].get("endpoints"):
        raise AuthError("No endpoints found for this account")
    session.endpoint_id = accounts[0]["endpoints"][0]["id"]
    session.initialized = True


def logout(session: _Session) -> None:
    try:
        session.http.get(BASE_URL + "/de/customer/logout")
    finally:
        session.initialized = False
        session.csrf_token = None
