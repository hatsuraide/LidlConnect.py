from typing import Any, Dict, List

from ._base import _BaseAPI
from .._helpers import ttl_cache, invalidate_cache


class SettingsAPI(_BaseAPI):

    @ttl_cache(60)
    def get_services(self) -> List[Dict[str, Any]]:
        """Service settings grouped by category (voicemail, calls/SMS, data, roaming)."""
        return self._post("/customer/settings/")

    @ttl_cache(30)
    def get_topup(self) -> Dict[str, Any]:
        """Auto top-up settings."""
        return self._post("/customer/settings/top-up-settings")

    @ttl_cache(300)
    def get_consents(self) -> Dict[str, Any]:
        """GDPR marketing consent settings."""
        return self._post("/customer/settings/consents")

    @ttl_cache(300)
    def get_egn(self) -> Dict[str, Any]:
        """Number masking settings (EGN): {maskPremiumNumbers, maskNonPremiumNumbers}."""
        return self._post("/customer/settings/egn-settings")

    def update_service(self, service_id: str, active: bool) -> bool:
        """Enable or disable a service by its ID (e.g. 'VOICEMAIL', 'VOICE_ROAMING').

        The full setting object for the given ID is fetched from get_services() first
        so the server receives the correct type and key fields.
        """
        setting = None
        for group in self.get_services():
            for s in group.get("settings", []):
                if s.get("id") == service_id:
                    setting = dict(s)
                    break
            if setting:
                break

        if setting is None:
            setting = {"id": service_id, "key": service_id, "type": "services"}

        setting["active"] = active
        setting["value"] = active
        self._post("/customer/settings/update-settings", {"setting": setting})
        invalidate_cache(self, SettingsAPI.get_services)
        return True

    def update_topup(self, settings: Dict[str, Any]) -> bool:
        """Update auto top-up settings.

        Pass a dict with keys such as enableThresholdTopup, thresholdTopupThreshold,
        thresholdTopupAmount, enablePriceBasedTopup.
        """
        self._post("/customer/settings/top-up-settings/update", settings)
        invalidate_cache(self, SettingsAPI.get_topup)
        return True

    def update_notifications(self, email_enabled: bool, sms_enabled: bool) -> bool:
        """Update notification channel preferences."""
        self._post(
            "/customer/settings/notifications/update",
            {"settings": {"emailEnabled": email_enabled, "smsEnabled": sms_enabled}},
        )
        return True

    def update_egn(self, mask_premium: bool, mask_non_premium: bool) -> bool:
        """Update number masking (EGN) settings."""
        self._post(
            "/customer/settings/egn-settings/update",
            {
                "maskPremiumNumbers": mask_premium,
                "maskNonPremiumNumbers": mask_non_premium,
            },
        )
        invalidate_cache(self, SettingsAPI.get_egn)
        return True

    def update_consents(self, consents: List[Dict]) -> bool:
        """Update GDPR consent list."""
        self._post("/customer/settings/consents/update", {"consents": consents})
        invalidate_cache(self, SettingsAPI.get_consents)
        return True
