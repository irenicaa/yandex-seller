from dataclasses import dataclass


@dataclass
class Credentials:
    oauth_client_id: str
    oauth_token: str

    def to_headers(self) -> dict[str, str]:
        return {
            "Authorization": "OAuth " \
                + f'oauth_token="{self.oauth_token}", ' \
                + f'oauth_client_id="{self.oauth_client_id}"',
        }
