from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


def main():
    uvicorn.run("app.main:app", reload=True)


if __name__ == "__main__":
    main()
