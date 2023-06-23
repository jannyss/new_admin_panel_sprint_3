import json
from typing import Any

from etl.utils.logger import logger
from .base_storage import BaseStorage


class JsonFileStorage(BaseStorage):
    """Storage implementation, which uses local .json file for storing.
    Storage format: JSON
    """

    def __init__(self, file_path: str = 'storage.json') -> None:
        self.file_path = file_path

    def save_state(self, state: dict[str, Any]) -> None:
        """Saves state to a storage."""
        with open(self.file_path, 'w') as file:
            file.write(json.dumps(state))

    def retrieve_state(self) -> dict[str, Any]:
        """Retrieves state from a storage."""
        try:
            with open(self.file_path, 'r') as file:
                state = file.read()
                return json.loads(state)
        except FileNotFoundError:
            logger.warning(f'File {self.file_path} not found! Initializing with empty dict and default file.')
            return {}
