import abc
from typing import Any


class BaseStorage(abc.ABC):
    """Abstract state storage.

     Allows saving and retrieving state.
     How state is stored can vary depending on
     from final implementation. For example, you can store information
     in a database or distributed file storage.
    """

    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """Saves state to a storage.."""

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """Retrieves state from a storage"""
