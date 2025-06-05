import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.repository.in_memory_repository import InMemoryRepository
from app.router import get_items_service
from app.router import router as items_router
from app.service import ItemsService


def mock_faulty_db_unexpected_error_repository():
    """Fixture to create a faulty repository that raises an error."""

    class FaultyRepository(InMemoryRepository):
        def list(self):
            raise Exception("Simulated database error")

        def get_by_id(self, key: str):
            raise Exception("Simulated item not found error")

        def add_item(self, value: str):
            raise Exception("failed_insert_value")

    return FaultyRepository()


def mock_in_memory_repository():
    """Fixture to create an in-memory repository with some initial data."""
    repository = InMemoryRepository()
    repository.add_item(value="String1")
    repository.add_item(value="String2")
    repository.add_item(value="String3")
    return repository


class MockService(ItemsService):
    """Mock service for testing purposes."""

    def __init__(self, repository=None):
        if repository is None:
            repository = InMemoryRepository()
        super().__init__(items_repository=repository)


@pytest.fixture
def client():
    """Fixture to create a TestClient for the FastAPI app."""
    app = FastAPI()
    app.include_router(items_router)

    service = MockService(repository=mock_in_memory_repository())

    def override_items_service():
        return service

    app.dependency_overrides[get_items_service] = override_items_service

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def faulty_db_client():
    """Fixture to create a TestClient for the FastAPI app."""
    app = FastAPI()
    app.include_router(items_router)

    service = MockService(repository=mock_faulty_db_unexpected_error_repository())

    def override_items_service():
        return service

    app.dependency_overrides[get_items_service] = override_items_service

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_get_all_items(client):
    """Test to ensure all items are retrieved correctly."""
    response = client.get("/items/")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0
    assert len(items) == 3


def test_get_item_by_id(client):
    """Test to ensure an item can be retrieved by its ID."""
    # First add a new item
    response = client.post("/items/", json={"value": "NewItem"})
    response_id = response.json().get("id")

    # Now retrieve the item by its ID
    response = client.get(f"/items/{response_id}")
    assert response.status_code == 200
    item = response.json()
    assert isinstance(item, dict)
    assert response_id in item
    assert item[response_id] == "NewItem"


def test_get_item_not_found(client):
    """Test to ensure an error is raised when an item is not found."""
    response = client.get("/items/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item with key 'nonexistent_id' not found."}


def test_add_item(client):
    """Test to ensure a new item can be added."""
    new_item = {"value": "NewItem"}
    response = client.post("/items/", json=new_item)
    assert response.status_code == 201
    result = response.json()
    assert "id" in result

    # Verify the item was added
    response = client.get(f"/items/{result['id']}")
    assert response.status_code == 200
    item = response.json()
    assert item[result["id"]] == "NewItem"


def test_add_item_validation_error(client):
    """Test to ensure adding an item with invalid data raises a validation error."""
    response = client.post("/items/", json={"invalid_field": "InvalidValue"})
    assert response.status_code == 422


def test_update_item(client):
    """Test to ensure an item can be updated."""
    # First add a new item
    response = client.post("/items/", json={"value": "ItemToUpdate"})
    response_id = response.json().get("id")

    # Update the item
    updated_value = "UpdatedItem"
    response = client.put(f"/items/{response_id}", json={"value": updated_value})
    assert response.status_code == 200

    # Verify the update
    response = client.get(f"/items/{response_id}")
    assert response.status_code == 200
    item = response.json()
    assert item[response_id] == updated_value


def test_update_item_not_found(client):
    """Test to ensure an error is raised when trying to update an item that does not exist."""
    response = client.put("/items/nonexistent_id", json={"value": "UpdatedValue"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item with key 'nonexistent_id' not found."}


def test_delete_item(client):
    """Test to ensure an item can be deleted."""
    # First add a new item
    response = client.post("/items/", json={"value": "ItemToDelete"})
    response_id = response.json().get("id")

    # Delete the item
    response = client.delete(f"/items/{response_id}")
    assert response.status_code == 204

    # Verify the item was deleted
    response = client.get(f"/items/{response_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Item with key '{response_id}' not found."}


def test_delete_item_not_found(client):
    """Test to ensure an error is raised when trying to delete an item that does not exist."""
    response = client.delete("/items/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item with key 'nonexistent_id' not found."}


def test_faulty_db_get_all_items(faulty_db_client):
    """Test to ensure an error is raised when the database operation fails."""
    response = faulty_db_client.get("/items/")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}


def test_faulty_db_add_invalid_item_expect_422(faulty_db_client):
    """Test to ensure an error is raised when adding an item with invalid data."""
    response = faulty_db_client.post("/items/", json={"invalid_field": "InvalidValue"})
    assert response.status_code == 422
