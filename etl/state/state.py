from typing import Any

from .base_storage import BaseStorage

STATE_KEY = 'last_movies_updated'


class State:
    """Class for work with states locally."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self.state = self.storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        """Set the state for a specific key."""
        if key in self.state:
            self.state[key] = value
            return
        self.state.update({key: value})
        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Any:
        """Get the state by a specific key."""
        return self.state.get(key, None)
