import requests

from .exceptions import InvalidToken


def validate_credentials_deepgram(TOKEN: str) -> bool:
    URL = "https://api.deepgram.com/v1/auth/token"
    response = requests.get(
        URL, headers={"Authorization": f"Token {TOKEN}"}, timeout=10
    )

    if response.status_code == 401:
        raise InvalidToken(
            f"The API token {TOKEN} is invalid! \nPlease check the token."
        )
    return True
