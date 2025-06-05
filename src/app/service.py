from pydantic import ValidationError as PydanticValidationError

from app.models import PostValue
from app.repository.base_repository import BaseRepository, DBError, DBItemNotFoundError


class ValidationError(Exception):
    """Exception raised for errors in user input."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ItemNotFoundError(Exception):
    """Exception raised when an item is not found."""

    def __init__(self, key):
        super().__init__(f"Item with key '{key}' not found.")
        self.key = key


class ServerError(Exception):
    """Exception raised for server errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ItemsService:
    def __init__(self, items_repository: BaseRepository):
        self.items_repository = items_repository

    def list(self):
        try:
            return self.items_repository.list()
        except DBError as e:
            # TODO: log DB error
            err_msg = f"Database error occurred: {str(e)}"
            raise ServerError(err_msg) from e
        except Exception as e:
            # TODO: log unexpected error
            err_msg = f"An unexpected error occurred: {str(e)}"
            raise ServerError(err_msg) from e

    def get_item_by_id(self, item_id: str):
        if not item_id:
            raise ValidationError("Item ID must be provided.")
        try:
            return self.items_repository.get_by_id(item_id)
        except DBItemNotFoundError as e:
            # TODO: log item not found error
            raise ItemNotFoundError(item_id) from e
        except DBError as e:
            # TODO: log DB error
            err_msg = f"Database error occurred: {str(e)}"
            raise ServerError(err_msg) from e
        except Exception as e:
            # TODO: log unexpected error
            err_msg = f"An unexpected error occurred: {str(e)}"
            raise ServerError(err_msg) from e

    def add_item(self, input_data: dict[str, str]):
        try:
            # Validate the item_data against PostValue model
            item = PostValue(**input_data)
            new_id: str = self.items_repository.add_item(item.value)
            return {"id": new_id}
        except PydanticValidationError as e:
            err_msg = "Invalid input data: "
            err_msg += "expected data in the format: {'value': 'string'}"
            err_msg += f" but got: {input_data}"
            raise ValidationError(err_msg) from e
        except DBError as e:
            # TODO: log DB error
            err_msg = f"Database error occurred: {str(e)}"
            raise ServerError(err_msg) from e
        except Exception as e:
            # TODO: log unexpected error
            err_msg = f"An unexpected error occurred: {str(e)}"
            raise ServerError(err_msg) from e

    def update_item(self, item_id: str, input_data: dict[str, str]):
        if not item_id:
            raise ValidationError("Item ID must be provided for update.")
        try:
            # Validate the item_data against PutValue model
            item = PostValue(**input_data)
            self.items_repository.update(item_id, item.value)
        except PydanticValidationError as e:
            err_msg = "Invalid input data: "
            err_msg += f"expected data in the format: {'value': 'string'}"
            err_msg += f" but got: {input_data.__dict__}"
            raise ValidationError(err_msg) from e
        except DBItemNotFoundError as e:
            raise ItemNotFoundError(item_id) from e
        except DBError as e:
            # TODO: log DB error
            err_msg = f"Database error occurred: {str(e)}"
            raise ServerError(err_msg) from e
        except Exception as e:
            # TODO: log unexpected error
            err_msg = f"An unexpected error occurred: {str(e)}"
            raise ServerError(err_msg) from e

    def delete_item(self, item_id: str):
        if not item_id:
            raise ValidationError("Item ID must be provided for deletion.")
        try:
            return self.items_repository.delete(item_id)
        except DBItemNotFoundError as e:
            raise ItemNotFoundError(item_id) from e
        except DBError as e:
            # TODO: log DB error
            err_msg = f"Database error occurred: {str(e)}"
            raise ServerError(err_msg) from e
        except Exception as e:
            # TODO: log unexpected error
            err_msg = f"An unexpected error occurred: {str(e)}"
            raise ServerError(err_msg) from e

    def head(self, n: int):
        if n <= 0:
            raise ValidationError(
                "The number of items to return must be greater than zero."
            )
        try:
            return self.items_repository.head(n)
        except DBError as e:
            # TODO: log DB error
            err_msg = f"Database error occurred: {str(e)}"
            raise ServerError(err_msg) from e
        except Exception as e:
            # TODO: log unexpected error
            err_msg = f"An unexpected error occurred: {str(e)}"
            print(err_msg)  # For debugging purposes
            raise ServerError(err_msg) from e

    def tail(self, n: int):
        if n <= 0:
            raise ValidationError(
                "The number of items to return must be greater than zero."
            )
        try:
            return self.items_repository.tail(n)
        except DBError as e:
            # TODO: log DB error
            err_msg = f"Database error occurred: {str(e)}"
            raise ServerError(err_msg) from e
        except Exception as e:
            # TODO: log unexpected error
            err_msg = f"An unexpected error occurred: {str(e)}"
            print(err_msg)
            raise ServerError(err_msg) from e
