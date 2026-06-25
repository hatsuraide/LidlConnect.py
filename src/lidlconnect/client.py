import atexit
import signal
from typing import Optional

from ._auth import login, init_session, logout
from ._session import _Session
from .api.credit import CreditAPI
from .api.invoices import InvoicesAPI
from .api.settings import SettingsAPI
from .api.tariffs import TariffsAPI
from .api.usage import UsageAPI
from .api.user import UserAPI


class LidlConnect:
    """Client for the Lidl Connect self-care portal.

    Usage::

        with LidlConnect("069012345678", puk="12345678") as client:
            print(client.user.name)
            print(client.usage.data)

    Or manually::

        client = LidlConnect("069012345678", puk="12345678")
        client.initialize()
        ...
        client.logout()
    """

    def __init__(
        self,
        identifier: str,
        puk: Optional[str] = None,
        password: Optional[str] = None,
    ):
        if not puk and not password:
            raise ValueError("Either puk or password must be provided")

        self._identifier = identifier
        self._token = puk or password
        self._use_puk = puk is not None

        self._session = _Session()

        self.user = UserAPI(self._session)
        self.usage = UsageAPI(self._session)
        self.tariffs = TariffsAPI(self._session)
        self.invoices = InvoicesAPI(self._session)
        self.settings = SettingsAPI(self._session)
        self.credit = CreditAPI(self._session)

        atexit.register(self._cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def initialize(self) -> "LidlConnect":
        """Login and fetch session tokens. Returns self for chaining."""
        login(self._session, self._identifier, self._token, self._use_puk)
        init_session(self._session)
        return self

    def logout(self) -> None:
        """Log out and invalidate the session."""
        if self._session.initialized:
            logout(self._session)

    # Context manager support
    def __enter__(self) -> "LidlConnect":
        return self.initialize()

    def __exit__(self, *_) -> None:
        self.logout()

    # Convenience passthrough properties
    @property
    def logged_in(self) -> bool:
        return self._session.initialized

    @property
    def user_id(self) -> Optional[int]:
        return self._session.user_id

    @property
    def endpoint_id(self) -> Optional[int]:
        return self._session.endpoint_id

    @property
    def csrf_token(self) -> Optional[str]:
        return self._session.csrf_token

    def _cleanup(self) -> None:
        if self._session.initialized:
            try:
                logout(self._session)
            except Exception:
                pass

    def _signal_handler(self, signum, frame) -> None:
        self._cleanup()
        signal.signal(signum, signal.SIG_DFL)
        signal.raise_signal(signum)
