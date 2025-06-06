from pydantic import ValidationError as PydanticValidationError

from app.common import logger
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
            logger.info("Listing all items")
            return self.items_repository.list()
        except DBError as e:
            err_msg = f"Database error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e
        except Exception as e:
            err_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e

    def get_item_by_id(self, item_id: str):
        if not item_id:
            logger.info(f"Getting item {item_id}")
            raise ValidationError("Item ID must be provided.")
        try:
            return self.items_repository.get_by_id(item_id)
        except DBItemNotFoundError as e:
            logger.error(str(e))
            raise ItemNotFoundError(item_id) from e
        except DBError as e:
            err_msg = f"Database error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e
        except Exception as e:
            err_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e

    def add_item(self, input_data: dict[str, str]):
        logger.info(f"Adding data from {input_data}")
        try:
            # Validate the item_data against PostValue model
            item = PostValue(**input_data)
            new_id: str = self.items_repository.add_item(item.value)
            return {"id": new_id}
        except PydanticValidationError as e:
            err_msg = "Invalid input data: "
            err_msg += "expected data in the format: {'value': 'string'}"
            err_msg += f" but got: {input_data}"
            logger.error(err_msg)
            raise ValidationError(err_msg) from e
        except DBError as e:
            err_msg = f"Database error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e
        except Exception as e:
            err_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e

    def update_item(self, item_id: str, input_data: dict[str, str]):
        logger.info(f"Update operation body: {input_data}, item_id: {item_id}")
        if not item_id:
            err_msg = "Item ID must be provided for update."
            logger.error(err_msg)
            raise ValidationError(err_msg)
        try:
            # Validate the item_data against PutValue model
            item = PostValue(**input_data)
            self.items_repository.update(item_id, item.value)
        except PydanticValidationError as e:
            err_msg = "Invalid input data: "
            err_msg += f"expected data in the format: {'value': 'string'}"
            err_msg += f" but got: {input_data.__dict__}"
            logger.error(err_msg)
            raise ValidationError(err_msg) from e
        except DBItemNotFoundError as e:
            logger.error(f"On update, item id; '{item_id}' was not found")
            raise ItemNotFoundError(item_id) from e
        except DBError as e:
            err_msg = f"Database error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e
        except Exception as e:
            err_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e

    def delete_item(self, item_id: str):
        if not item_id:
            err_msg = "Item ID must be provided for deletion. Received None"
            logger.error(err_msg)
            raise ValidationError(err_msg)
        try:
            return self.items_repository.delete(item_id)
        except DBItemNotFoundError as e:
            logger.error(f"On delete, item id; '{item_id}' was not found")
            raise ItemNotFoundError(item_id) from e
        except DBError as e:
            err_msg = f"Database error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e
        except Exception as e:
            err_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e

    def head(self, n: int):
        if n <= 0:
            err_msg = "head: The number of items to return must be greater than zero."
            logger.error(err_msg)
            raise ValidationError(err_msg)
        try:
            return self.items_repository.head(n)
        except DBError as e:
            err_msg = f"Database error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e
        except Exception as e:
            err_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e

    def tail(self, n: int):
        if n <= 0:
            err_msg = "tail: The number of items to return must be greater than zero."
            raise ValidationError(err_msg)
        try:
            return self.items_repository.tail(n)
        except DBError as e:
            err_msg = f"Database error occurred: {str(e)}"
            logger.error(err_msg)
            raise ServerError(err_msg) from e
        except Exception as e:
            err_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(err_msg)

            raise ServerError(err_msg) from e
