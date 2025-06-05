from fastapi import FastAPI

from app.router import router as items_router

api = FastAPI(
    title="Stings API",
    description="API for managing a collection of strings",
    version="1.0.0",
)
api.include_router(items_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api)
