import requests
from typing import Optional

BASE_URL = "https://selfcare.lidl-connect.at"
_DASHBOARD_URL = BASE_URL + "/customer/dashboard/"


class _Session:
    def __init__(self):
        self.http = requests.Session()
        self.http.headers.update({"User-Agent": "Mozilla/5.0"})
        self.csrf_token: Optional[str] = None
        self.user_id: Optional[int] = None
        self.endpoint_id: Optional[int] = None
        self.initialized: bool = False

    def api_headers(self, extra: Optional[dict] = None) -> dict:
        h = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": BASE_URL,
            "Referer": _DASHBOARD_URL,
            "X-CSRF-TOKEN": self.csrf_token or "",
            "X-SELF-CARE": "1",
        }
        if extra:
            h.update(extra)
        return h

    @property
    def base_payload(self) -> dict:
        return {"userId": self.user_id, "endpointId": self.endpoint_id}
