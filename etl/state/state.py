from typing import Any

from utils.logger import logger
from .base_storage import BaseStorage

STATE_KEY = 'last_movies_updated'


class State:
    """Class for work with states locally."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self.state = self.storage.retrieve_state()
        logger.info('Local state was initialized')

    def set_state(self, key: str, value: Any) -> None:
        """Set the state for a specific key."""
        if key in self.state:
            self.state[key] = value
            return
        self.state.update({key: value})
        self.storage.save_state(self.state)
        logger.info(f'State "{key}: {value}" was set')

    def get_state(self, key: str) -> Any:
        """Get the state by a specific key."""
        state = self.state.get(key, None)
        logger.info(f'Got state: {state} for key: {key}')
        return state
