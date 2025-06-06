import threading
import time
from typing import Optional

import requests

from ms_sample_list_creator.implementations.result import Result
from ms_sample_list_creator.structure import DirectusCredentials


class TokenManager:
    _instance: Optional["TokenManager"] = None

    def __new__(cls, credentials: Optional[DirectusCredentials] = None) -> "TokenManager":
        if cls._instance is None:
            if credentials is None:
                raise ValueError("TokenManager requires credentials on first initialization.")
            cls._instance = super().__new__(cls)
            cls._instance._init(credentials)
        return cls._instance

    def _init(self, credentials: DirectusCredentials) -> None:
        self.credentials = credentials
        self.token: Optional[str] = None
        self.expiry: float = 0.0
        self.lock: threading.Lock = threading.Lock()
        self._start_auto_refresh()

    def get_token(self) -> Optional[str]:
        with self.lock:
            return self.token

    def refresh_token(self) -> Result[None, str]:
        with self.lock:
            result = get_directus_token(self.credentials)
            if result.is_ok:
                self.token = result.value
                self.expiry = time.time() + 15 * 60  # valid for 15 minutes
                return Result(value=None)
            else:
                print("❌ Failed to refresh token:", result.error)
                return Result(error=result.error)

    def _start_auto_refresh(self) -> None:
        def refresh_loop() -> None:
            while True:
                self.refresh_token()
                time.sleep(14 * 60)  # Refresh every 14 minutes

        thread = threading.Thread(target=refresh_loop, daemon=True)
        thread.start()


def get_directus_token(credentials: DirectusCredentials) -> Result[str, str]:
    """
    Attempts to connect to Directus using the provided user data.

    If the connection is successful, the access token is stored.

    Args:
        user_data (dict): The dictionary containing the necessary user data.

    Returns:
        None
    """

    base_url = "https://emi-collection.unifr.ch/directus"
    login_url = base_url + "/auth/login"

    try:
        response = requests.post(
            login_url, json={"email": credentials.username, "password": credentials.password}, timeout=10
        )
        response.raise_for_status()

        return Result(value=response.json()["data"]["access_token"])

    except requests.HTTPError as e:
        return Result(error=f"HTTPError during Directus login: {e}")

    except requests.RequestException as e:
        return Result(error=f"RequestException during Directus login: {e}")


def validate_credentials(credentials: DirectusCredentials) -> Result[str, str]:
    """
    Validates Directus credentials without affecting the global TokenManager instance.

    Args:
        credentials (DirectusCredentials): The credentials to validate.

    Returns:
        Result[str, str]: The result of the token request attempt.
    """
    return get_directus_token(credentials)
