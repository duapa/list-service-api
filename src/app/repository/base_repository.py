from abc import ABC, abstractmethod
from typing import List


class DBError(Exception):
    """Base class for all database-related exceptions."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DBItemNotFoundError(DBError):
    """Exception raised when an item is not found in the repository."""

    def __init__(self, key):
        super().__init__(f"Item with key '{key}' not found.")
        self.key = key


class DBFailedToAddItemError(DBError):
    """Exception raised when an item fails to be added to the repository."""

    def __init__(self, value):
        super().__init__(f"Failed to add item with value '{value}'.")
        self.value = value


class DBFailedToUpdateItemError(DBError):
    """Exception raised when an item fails to be updated in the repository."""

    def __init__(self, key, value):
        super().__init__(f"Failed to update item with key '{key}' and value '{value}'.")
        self.key = key
        self.value = value


class DBFailedtoListItemsError(DBError):
    """Exception raised when the list all items operation fails."""

    def __init__(self, message):
        super().__init__(f"Failed to list items: {message}")
        self.message = message


class DBFailedToDeleteItemError(DBError):
    """Exception raised when an item fails to be deleted from the repository."""

    def __init__(self, key):
        super().__init__(f"Failed to delete item with key '{key}'.")
        self.key = key


class DBFailedToCountItemsError(DBError):
    """Exception raised when counting items in the repository fails."""

    def __init__(self, message):
        super().__init__(f"Failed to count items: {message}")
        self.message = message


class BaseRepository(ABC):
    @abstractmethod
    def get_by_id(self, key) -> dict[str, str]:
        """Retrieve an item by its key."""
        raise NotImplementedError("This method should be overridden in a subclass.")

    @abstractmethod
    def add_item(self, value: str) -> str:
        """Add a new item to the repository."""
        raise NotImplementedError("This method should be overridden in a subclass.")

    @abstractmethod
    def update(self, key: str, value: str) -> None:
        """Set an item with a key and value."""
        raise NotImplementedError("This method should be overridden in a subclass.")

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete an item by its key."""
        raise NotImplementedError("This method should be overridden in a subclass.")

    @abstractmethod
    def list(self) -> List[dict[str, str]]:
        """List all items."""
        raise NotImplementedError("This method should be overridden in a subclass.")

    @abstractmethod
    def head(self, n: int) -> List[dict[str, str]]:
        """Get the top N elements of the list."""
        raise NotImplementedError("This method should be overridden in a subclass.")

    @abstractmethod
    def tail(self, n: int) -> List[dict[str, str]]:
        """Get the bottom N elements of the list."""
        raise NotImplementedError("This method should be overridden in a subclass.")

    @abstractmethod
    def count(self) -> int:
        """Count the number of items in the repository."""
        raise NotImplementedError("This method should be overridden in a subclass.")
