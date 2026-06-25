from typing import Any, Dict, List, Optional

from ._base import _BaseAPI
from .._helpers import ttl_cache


def _find_counter(groups: List[Dict], counter_id: str) -> Dict[str, Any]:
    for group in groups:
        for elem in group.get("instanceElements", []):
            for counter in elem.get("counters", []):
                if counter.get("counterId") == counter_id:
                    nv = counter.get("niceValue", {})
                    bv = counter.get("baseValue", {})
                    total = nv.get("initialValue", 0)
                    remaining = nv.get("value", 0)
                    return {
                        "remaining": remaining,
                        "total": total,
                        "used": total - remaining,
                        "unit": nv.get("type") or bv.get("type", ""),
                    }
    return {"remaining": 0, "total": 0, "used": 0, "unit": ""}


class UsageAPI(_BaseAPI):

    @ttl_cache(30)
    def get(self) -> Dict[str, Any]:
        """Raw usage data from /customer/usage/."""
        return self._post("/customer/usage/")

    def _groups(self) -> List[Dict]:
        return self.get().get("instanceGroups", [])

    def _tariff_package(self) -> Optional[Dict]:
        for group in self._groups():
            if group.get("itemCategory") == "TARIFF_PACKAGE":
                return group
        return None

    @property
    def data(self) -> Dict[str, Any]:
        """Domestic data: {remaining, total, used, unit}."""
        return _find_counter(self._groups(), "DATA")

    @property
    def eu_data(self) -> Dict[str, Any]:
        """EU roaming data: {remaining, total, used, unit}."""
        return _find_counter(self._groups(), "DATA_EU")

    @property
    def minutes(self) -> Dict[str, Any]:
        """Voice/SMS minutes: {remaining, total, used, unit}."""
        return _find_counter(self._groups(), "VOICE_SMS")

    @property
    def international_minutes(self) -> Dict[str, Any]:
        """International minutes: {remaining, total, used, unit}."""
        return _find_counter(self._groups(), "VOICE_SMS_INT")

    @property
    def tariff_name(self) -> Optional[str]:
        pkg = self._tariff_package()
        return pkg.get("itemName") if pkg else None

    @property
    def valid_from(self) -> Optional[str]:
        pkg = self._tariff_package()
        elems = (pkg or {}).get("instanceElements", [])
        return elems[0].get("validFrom") if elems else None

    @property
    def valid_to(self) -> Optional[str]:
        pkg = self._tariff_package()
        elems = (pkg or {}).get("instanceElements", [])
        return elems[0].get("validTo") if elems else None

    @property
    def next_renewal(self) -> Optional[str]:
        pkg = self._tariff_package()
        return (pkg or {}).get("nextProlongation")

    @property
    def gross_price(self) -> Optional[float]:
        pkg = self._tariff_package()
        elems = (pkg or {}).get("instanceElements", [])
        return elems[0].get("grossPrice") if elems else None

    @property
    def download_speed(self) -> Optional[int]:
        """Download speed limit in bytes/sec (from QoS profile)."""
        for profile in self.get().get("qosProfiles", {}).values():
            v = profile.get("qosValues", {}).get("DOWNLOAD_SPEED_IN_BYTES_PER_SEC")
            return int(v) if v else None
        return None

    @property
    def upload_speed(self) -> Optional[int]:
        """Upload speed limit in bytes/sec (from QoS profile)."""
        for profile in self.get().get("qosProfiles", {}).values():
            v = profile.get("qosValues", {}).get("UPLOAD_SPEED_IN_BYTES_PER_SEC")
            return int(v) if v else None
        return None

    @property
    def queued(self) -> List[Dict]:
        """Packages queued for activation."""
        return self.get().get("queues", [])
