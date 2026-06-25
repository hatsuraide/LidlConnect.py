from typing import Any, Dict, List, Optional

from ._base import _BaseAPI
from .._helpers import ttl_cache
from .._session import BASE_URL


class InvoicesAPI(_BaseAPI):

    @ttl_cache(60)
    def get_invoices(self) -> List[Dict[str, Any]]:
        """Payment invoices (card/banking top-ups)."""
        data = self._post(
            "/customer/invoices/invoice-list",
            {"accountId": self._s.endpoint_id},
        )
        return data if isinstance(data, list) else []

    @ttl_cache(60)
    def get_vouchers(self) -> List[Dict[str, Any]]:
        """Consumed scratch-card vouchers."""
        data = self._post("/customer/invoices/consumed-vouchers")
        return data if isinstance(data, list) else []

    def get_calls(self, page: int = 1, size: int = 50) -> Dict[str, Any]:
        """Itemised call/SMS/data event log. Returns {events, count, filtered}."""
        return self._post("/customer/invoices/call-list", {"page": page, "size": size})

    def get_config(self) -> Dict[str, Any]:
        """Invoice display config (months to display, available list types)."""
        return self._post("/customer/invoices/config")

    @ttl_cache(120)
    def get_timeline(self) -> Dict[str, Any]:
        """Unified timeline of all usage events."""
        return self._post("/customer/timeline/")

    def download_calls(self) -> bytes:
        """Download call list as binary (PDF/CSV depending on server)."""
        self._ensure_init()
        r = self._s.http.get(
            BASE_URL + f"/customer/invoices/download-calls/{self._s.endpoint_id}",
            headers=self._s.api_headers(),
        )
        r.raise_for_status()
        return r.content

    def total_spent(self) -> float:
        """Sum of all invoice amounts and voucher values in euros."""
        total = sum(i.get("amount", 0) for i in self.get_invoices())
        total += sum(v.get("balanceAdvice", 0) for v in self.get_vouchers())
        return total

    @property
    def last_payment_date(self) -> Optional[str]:
        dates = [i["postingDate"] for i in self.get_invoices() if i.get("postingDate")]
        dates += [v["consumedDate"] for v in self.get_vouchers() if v.get("consumedDate")]
        return max(dates) if dates else None
