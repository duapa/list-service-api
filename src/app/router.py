from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from app.models import PostValue
from app.repository.in_memory_repository import InMemoryRepository
from app.service import ItemNotFoundError, ItemsService, ServerError, ValidationError

router = APIRouter()


service = ItemsService(items_repository=InMemoryRepository())


def get_items_service() -> ItemsService:
    """Dependency to provide the ItemsService instance."""
    return service


@router.get("/items")
async def get_items(service: Annotated[ItemsService, Depends(get_items_service)]):
    try:
        results = service.list()
        return JSONResponse(
            results,
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except (ServerError, Exception):
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@router.get("/items/{item_id}")
async def get_item(
    item_id: str, service: Annotated[ItemsService, Depends(get_items_service)]
):
    try:
        item = service.get_item_by_id(item_id)
        return JSONResponse(
            item,
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except ItemNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except ServerError:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@router.post("/items")
async def add_item(
    input_data: PostValue, service: Annotated[ItemsService, Depends(get_items_service)]
):
    try:
        new_item = service.add_item(input_data.model_dump())
        return JSONResponse(
            new_item,
            status_code=201,
            headers={"Content-Type": "application/json"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except ServerError:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@router.put("/items/{item_id}")
async def update_item(
    item_id: str,
    input_data: PostValue,
    service: Annotated[ItemsService, Depends(get_items_service)],
):
    try:
        updated_item = service.update_item(
            item_id=item_id, input_data=input_data.model_dump()
        )
        return JSONResponse(
            updated_item,
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except ItemNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except ServerError:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: str, service: Annotated[ItemsService, Depends(get_items_service)]
):
    try:
        service.delete_item(item_id)
        return JSONResponse(
            {"message": "Item deleted successfully"},
            status_code=204,
            headers={"Content-Type": "application/json"},
        )
    except ItemNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except ServerError:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@router.get("/tail")
async def get_tail_items(
    service: Annotated[ItemsService, Depends(get_items_service)],
    num_samples: int = Query(10, ge=1),
):
    try:
        results = service.tail(num_samples)
        return JSONResponse(
            results,
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except (ServerError, Exception):
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@router.get("/head")
async def get_head_items(
    service: Annotated[ItemsService, Depends(get_items_service)],
    num_samples: int = Query(10, ge=1),
):
    try:
        results = service.head(num_samples)
        return JSONResponse(
            results,
            status_code=200,
            headers={"Content-Type": "application/json"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except (ServerError, Exception):
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )
