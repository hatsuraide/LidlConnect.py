from typing import Any, Dict, List, Optional

from ._base import _BaseAPI
from .._session import BASE_URL
from ..exceptions import APIError


class CreditAPI(_BaseAPI):

    def topup(self, code: str) -> bool:
        """Redeem a voucher/scratch-card code."""
        phone = self._phone_number()
        r = self._s.http.post(
            BASE_URL + "/credit/code",
            headers=self._s.api_headers(),
            json={
                "phoneNumber": phone,
                "code": {
                    "label": "credit_top_up.bon",
                    "code_fields": 1,
                    "code_field_length": 16,
                    "code_validation": "^([a-zA-Z0-9]+)$",
                    "active": True,
                    "api_type": "VOUCHER_WITH_ACTIVATION_NUMBER",
                    "code": code,
                },
                "userId": self._s.user_id,
                "endpointId": self._s.endpoint_id,
            },
        )
        if not r.ok:
            raise APIError(r.status_code, r.text)
        return True

    def get_balance(self) -> Dict[str, float]:
        """Current account balance: {balance, bonusBalance}."""
        return self._post("/customer/tariffs/endpoint-balance")

    def get_payment_channels(self, phone_number: Optional[str] = None) -> List[Dict[str, Any]]:
        """Available payment channels (card, banking, etc.).

        Args:
            phone_number: Phone number in API format (e.g. '4369012345678').
                          Defaults to the authenticated account's number.
        """
        return self._post(
            "/credit/fetch-payment-channels",
            {"phoneNumber": phone_number or self._phone_number()},
        )

    def _phone_number(self) -> str:
        from .user import UserAPI
        ep = UserAPI(self._s)._endpoint()
        if not ep:
            raise ValueError("Could not determine phone number for credit operation")
        return ep.get("name", "")
