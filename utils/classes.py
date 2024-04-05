from dataclasses import dataclass


@dataclass
class UserInputs:
    plex_url: str
    plex_token: str
    library_names: str
    ignore_list: str
    wait_seconds: int
