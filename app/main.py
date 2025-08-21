from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, status
from typing import Any
from scalar_fastapi import get_scalar_api_reference
# from sqlmodel import Session
from app.schemas import Shipment,ShipmentCreate,ShipmentUpdate,ShipmentStatus
# from app.database import Database
from app.database.session import create_db_tables, SessionDep
from contextlib import asynccontextmanager
from app.api.router import router
# from app.database.models import Shipment

@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    print("server is starting")
    create_db_tables()
    yield
    print("server is shutting down")

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )
