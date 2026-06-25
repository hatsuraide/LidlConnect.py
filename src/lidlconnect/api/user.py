from typing import Any, Dict, List, Optional

from ._base import _BaseAPI
from .._helpers import ttl_cache


class UserAPI(_BaseAPI):

    @ttl_cache(30)
    def get(self) -> Dict[str, Any]:
        """Raw user data from /customer/dashboard/login-check."""
        return self._post("/customer/dashboard/login-check")

    def _endpoint(self) -> Optional[Dict[str, Any]]:
        for account in self.get().get("accounts", []):
            for ep in account.get("endpoints", []):
                if ep.get("id") == self._s.endpoint_id:
                    return ep
        return None

    @property
    def name(self) -> Optional[str]:
        return self.get().get("name")

    @property
    def phone_number(self) -> Optional[str]:
        """Phone number as returned by the API (e.g. '4369012345678')."""
        ep = self._endpoint()
        return ep.get("name") if ep else None

    @property
    def balance(self) -> Optional[float]:
        ep = self._endpoint()
        return ep.get("ocsBalance") if ep else None

    @property
    def bonus_balance(self) -> Optional[float]:
        ep = self._endpoint()
        return ep.get("ocsBonusBalance") if ep else None

    @property
    def status(self) -> Optional[str]:
        ep = self._endpoint()
        return ep.get("status") if ep else None

    @property
    def has_password(self) -> bool:
        return bool(self.get().get("hasPassword"))

    @property
    def birth_date(self) -> Optional[str]:
        return self.get().get("birthDate")

    @property
    def customer_type(self) -> Optional[str]:
        return self.get().get("customerType")

    @property
    def customer_language(self) -> Optional[str]:
        return self.get().get("customerLanguage")

    @property
    def activation_date(self) -> Optional[str]:
        ep = self._endpoint()
        return ep.get("activationDate") if ep else None

    @property
    def deactivation_date(self) -> Optional[str]:
        ep = self._endpoint()
        return ep.get("deactivationDate") if ep else None

    @property
    def imsi(self) -> Optional[str]:
        ep = self._endpoint()
        imsis: List[Dict] = (ep or {}).get("imsis", [])
        return imsis[0].get("imsi") if imsis else None

    @property
    def iccid(self) -> Optional[str]:
        ep = self._endpoint()
        imsis: List[Dict] = (ep or {}).get("imsis", [])
        return imsis[0].get("iccid") if imsis else None

    @property
    def is_esim(self) -> bool:
        ep = self._endpoint()
        imsis: List[Dict] = (ep or {}).get("imsis", [])
        return bool(imsis[0].get("esim")) if imsis else False

    @property
    def notification_settings(self) -> Optional[Dict[str, Any]]:
        return self.get().get("notificationSettings")

    @property
    def topup_settings(self) -> Optional[Dict[str, Any]]:
        for account in self.get().get("accounts", []):
            if account.get("id") == self._s.endpoint_id:
                return account.get("topupSettings")
        return None
