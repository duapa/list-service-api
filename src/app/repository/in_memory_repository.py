import itertools
from typing import List
from uuid import uuid4

from .base_repository import (
    BaseRepository,
    DBFailedToAddItemError,
    DBFailedToCountItemsError,
    DBFailedToDeleteItemError,
    DBFailedtoListItemsError,
    DBFailedToUpdateItemError,
    DBItemNotFoundError,
)


class InMemoryRepository(BaseRepository):
    def __init__(self, data: dict[str, str] = {}):
        self._data: dict[str, str] = data or {}

    def get_by_id(self, key: str) -> dict[str, str]:
        """Retrieve an item by its key."""

        if key not in self._data:
            raise DBItemNotFoundError("Could not find item with key: {}".format(key))
        # Return a dictionary with the key and its corresponding value
        return {key: self._data[key]}

    def add_item(self, value: str) -> str:
        key = str(uuid4())

        try:
            self._data[key] = value
        except Exception as e:
            raise DBFailedToAddItemError(value) from e
        return key

    def update(self, key, value):
        if key not in self._data:
            raise DBItemNotFoundError(key)
        try:
            self._data[key] = value
        except Exception as e:
            raise DBFailedToUpdateItemError(key, value) from e

    def delete(self, key: str):
        if key not in self._data:
            raise DBItemNotFoundError(key)
        try:
            del self._data[key]
        except Exception as e:
            raise DBFailedToDeleteItemError(key) from e

    def list(self):
        """List all items in the repository."""
        return self.format_results(self._data)

    def head(self, n: int):
        _num_samples = n
        if self.count() <= 0:
            return []
        elif self.count() <= n:
            _num_samples = self.count()

        try:
            results = itertools.islice(self._data.items(), _num_samples)
            return self.format_results(dict(results))
        except Exception as e:
            raise DBFailedtoListItemsError("Head operation failed.") from e

    def tail(self, n: int):
        _num_samples = n
        if self.count() <= 0:
            return []
        elif self.count() <= n:
            _num_samples = self.count()

        try:
            results = itertools.islice(reversed(self._data.items()), _num_samples)
            return self.format_results(dict(results))
        except Exception as e:
            raise DBFailedtoListItemsError("Tail operation failed.") from e

    def count(self) -> int:
        try:
            return len(self._data)
        except Exception as e:
            raise DBFailedToCountItemsError("") from e

    def format_results(self, results: dict[str, str]) -> List[dict[str, str]]:
        """Format the results into a list of dictionaries."""
        formatted_results = []
        for key, value in results.items():
            formatted_results.append({"id": key, "value": value})
        return formatted_results
