from typing import Any, Dict, List

from ._base import _BaseAPI
from .._helpers import ttl_cache


class TariffsAPI(_BaseAPI):

    @ttl_cache(60)
    def get_available(self) -> List[Dict[str, Any]]:
        """All tariff options from the CMS (name, description, pricing, translations)."""
        data = self._post("/customer/tariffs/all-packages")
        return [p for p in data if p.get("category") == "TARIFF"]

    @ttl_cache(30)
    def get_switchable(self) -> List[Dict[str, Any]]:
        """Tariffs you can switch to at the start of the next billing cycle."""
        return self._post("/customer/tariffs/switchable-packages").get("tariffs", [])

    @ttl_cache(30)
    def get_purchasable(self) -> List[Dict[str, Any]]:
        """Add-on packages available for immediate purchase."""
        return self._post("/customer/tariffs/purchasable-packages").get("packages", [])

    def get_balance(self) -> Dict[str, float]:
        """Account balance: {balance, bonusBalance}."""
        return self._post("/customer/tariffs/endpoint-balance")

    def switch(self, item_id: str) -> bool:
        """Schedule a tariff switch for the next billing cycle."""
        self._post("/customer/tariffs/switch-package", {"itemId": item_id})
        return True

    def buy(self, item_id: str) -> bool:
        """Buy an add-on package immediately."""
        self._post("/customer/tariffs/buy-package", {"itemId": item_id})
        return True
