import pytest

from app.repository.in_memory_repository import (
    DBFailedToAddItemError,
    DBFailedtoListItemsError,
    DBItemNotFoundError,
    InMemoryRepository,
)
from app.service import ItemNotFoundError, ItemsService, ServerError, ValidationError


@pytest.fixture
def items_service():
    """Fixture to create a Service instance with an InMemoryRepository."""
    repository = InMemoryRepository()
    repository.add_item(value="String1")
    repository.add_item(value="String2")
    repository.add_item(value="String3")
    return ItemsService(items_repository=repository)


@pytest.fixture
def faulty_db_error_repository():
    """Fixture to create a faulty repository that raises an error."""

    class FaultyRepository(InMemoryRepository):
        def list(self):
            raise DBFailedtoListItemsError("Simulated database error")

        def get_by_id(self, key: str):
            raise DBItemNotFoundError("Simulated item not found error")

        def add_item(self, value: str):
            raise DBFailedToAddItemError("failed_insert_value")

    return FaultyRepository()


@pytest.fixture
def faulty_db_unexpected_error_repository():
    """Fixture to create a faulty repository that raises an error."""

    class FaultyRepository(InMemoryRepository):
        def list(self):
            raise Exception("Simulated database error")

        def get_by_id(self, key: str):
            raise Exception("Simulated item not found error")

        def add_item(self, value: str):
            raise Exception("failed_insert_value")

    return FaultyRepository()


def test_get_all_items(items_service):
    """Test to ensure all items are retrieved correctly."""
    items = items_service.list()
    assert len(items) == 3
    assert items[0]["value"] == "String1"
    assert items[1]["value"] == "String2"
    assert items[2]["value"] == "String3"


def test_get_item_by_id(items_service):
    """Test to ensure an item can be retrieved by its ID."""
    result = items_service.add_item({"value": "NewItem"})
    item_id = result["id"]
    item = items_service.get_item_by_id(item_id)
    assert item[item_id] == "NewItem"


def test_add_item(items_service):
    """Test to ensure a new item can be added."""
    new_item = {"value": "NewItem"}
    result = items_service.add_item(new_item)
    assert result is not None
    item_id = result["id"]
    item = items_service.get_item_by_id(item_id)
    assert item[item_id] == "NewItem"


def test_add_item_validation_error(items_service):
    """Test to ensure adding an item with invalid data raises a validation error."""
    with pytest.raises(ValidationError):
        items_service.add_item({"invalid_field": "InvalidValue"})


def test_get_item_by_id_not_found(items_service):
    """Test to ensure an error is raised when trying to get an item that does not exist."""
    with pytest.raises(ItemNotFoundError):
        items_service.get_item_by_id("non_existent_id")


def test_update_item(items_service):
    """Test to ensure an item can be updated."""
    new_item = {"value": "ItemToUpdate"}
    result = items_service.add_item(new_item)
    item_id = result["id"]

    # Update the item
    updated_value = "UpdatedItem"
    items_service.update_item(item_id, {"value": updated_value})

    # Verify the update
    item = items_service.get_item_by_id(item_id)
    assert item[item_id] == updated_value


def test_update_item_not_found(items_service):
    """Test to ensure an error is raised when trying to update an item that does not exist."""
    with pytest.raises(ItemNotFoundError):
        items_service.update_item("non_existent_id", {"value": "NewValue"})


def test_delete_item(items_service):
    """Test to ensure an item can be deleted."""
    new_item = {"value": "ItemToDelete"}
    result = items_service.add_item(new_item)
    item_id = result["id"]

    # Delete the item
    items_service.delete_item(item_id)

    # Verify the item is deleted
    with pytest.raises(ItemNotFoundError):
        items_service.get_item_by_id(item_id)


def test_delete_item_not_found(items_service):
    """Test to ensure an error is raised when trying to delete an item that does not exist."""
    with pytest.raises(ItemNotFoundError):
        items_service.delete_item("non_existent_id")


def test_list_items_db_error(faulty_db_error_repository):
    """Test to ensure a server error is raised when listing items fails."""
    service = ItemsService(items_repository=faulty_db_error_repository)
    with pytest.raises(ServerError) as exc_info:
        service.list()
    assert "Database error occurred" in str(exc_info.value)


def test_list_items_db_unexpected_error(faulty_db_unexpected_error_repository):
    """Test to ensure a server error is raised when listing items fails."""
    service = ItemsService(items_repository=faulty_db_unexpected_error_repository)
    with pytest.raises(ServerError) as exc_info:
        service.list()
    assert "An unexpected error occurred" in str(exc_info.value)


def test_head(items_service):
    results = items_service.head(3)
    expected = ["String1", "String2", "String3"]
    values = [item["value"] for item in results]
    assert values == expected


def test_tail(items_service):
    results = items_service.tail(3)
    expected = ["String3", "String2", "String1"]
    values = [item["value"] for item in results]
    assert values == expected


def test_head_sample_count_greater_than_list_len(items_service):
    results = items_service.head(5)
    expected = ["String1", "String2", "String3"]
    values = [item["value"] for item in results]
    assert values == expected


def test_tail_sample_count_greater_than_list_len(items_service):
    results = items_service.tail(3)
    expected = ["String3", "String2", "String1"]
    values = [item["value"] for item in results]
    assert values == expected


def test_head_sample_assert_sample_count_zero_raises_validation_error(items_service):
    with pytest.raises(ValidationError):
        _ = items_service.head(0)


def test_tail_sample_assert_sample_count_zero_raises_validation_error(items_service):
    with pytest.raises(ValidationError):
        _ = items_service.tail(0)
