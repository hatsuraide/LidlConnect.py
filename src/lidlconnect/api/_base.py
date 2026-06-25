from typing import Any, Optional

from .._session import _Session, BASE_URL
from ..exceptions import APIError, NotInitializedError


class _BaseAPI:
    def __init__(self, session: _Session):
        self._s = session

    def _ensure_init(self) -> None:
        if not self._s.initialized:
            raise NotInitializedError("Call client.initialize() before using the API")

    def _post(self, path: str, extra: Optional[dict] = None) -> Any:
        self._ensure_init()
        data = {**self._s.base_payload, **(extra or {})}
        r = self._s.http.post(BASE_URL + path, headers=self._s.api_headers(), json=data)
        if not r.ok:
            raise APIError(r.status_code, r.text)
        return r.json() if r.text.strip() else None

    def _get(self, path: str, params: Optional[dict] = None) -> Any:
        self._ensure_init()
        r = self._s.http.get(
            BASE_URL + path, headers=self._s.api_headers(), params=params
        )
        if not r.ok:
            raise APIError(r.status_code, r.text)
        return r.json() if r.text.strip() else None
