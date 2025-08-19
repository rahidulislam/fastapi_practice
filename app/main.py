from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, status
from typing import Any
from scalar_fastapi import get_scalar_api_reference
# from sqlmodel import Session
from app.schemas import Shipment,ShipmentCreate,ShipmentUpdate,ShipmentStatus
# from app.database import Database
from app.database.session import create_db_tables, SessionDep
from contextlib import asynccontextmanager
# from app.database.models import Shipment

@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    print("server is starting")
    create_db_tables()
    yield
    print("server is shutting down")

app = FastAPI(lifespan=lifespan_handler)
# db= Database()

# shipments = {
#     1: {"content": "Books", "weight": 3, "status": "in_transit","destination": 1234},
#     2: {"content": "Electronics", "weight": 5, "status": "delivered", "destination": 1234},
#     3: {"content": "Clothes", "weight": 2, "status": "placed", "destination": 1234},
#     4: {"content": "Furniture", "weight": 15, "status": "delivered", "destination": 1234},
#     5: {"content": "Toys", "weight": 4, "status": "out_for_delivery", "destination": 1234},
# }



@app.get("/shipment", response_model=Shipment)
def get_shipment_list(id: int | None = None, session: SessionDep=None):
    shipment= session.get(Shipment, id)
    # if not id:
    #     id = max(shipments.keys())
    #     return shipments[id]
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment is not found"
        )
    
    return shipment


# @app.get("/shipment/{field}")
# def get_shipment_field(field: str, id: int) -> dict[str, Any]:
#     return {field: shipments[id][field]}


# @app.get("/shipment/{id}")
# def get_shipment_data(id: int):
#     if id not in shipments:
#         raise HTTPException(status_code=404, detail="Shipment not found")
#     shipment= shipments[id]
#     return Shipment(**shipment)


@app.post("/shipment")
def create_shipment(shipment: ShipmentCreate, session:SessionDep) -> dict[str,int]:
    
    # if shipment.weight > 25:
    #     raise HTTPException(
    #         status_code=400, detail="Weight exceeds maximum limit of 25kg"
    #     )
    # new_id = max(shipments.keys()) + 1
    # shipments[new_id] = {
    #     "content": shipment.content,
    #     "weight": shipment.weight,
    #     "status": "placed",
    #     "destination": shipment.destination
    # }
    # shipments[new_id] = {
    #     **shipment.model_dump(),
    #     "status": "placed",
    #     "id": new_id
    # }
    # save()
    # new_id = db.create(shipment)
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3)  # Example estimated delivery
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id":new_shipment.id}


# @app.put("/shipment")
# def shipment_update(
#     id: int, content: str, weight: float, status: str
# ) -> dict[str, Any]:
#     shipments[id] = {"content": content, "weight": weight, "status": status}
#     return shipments[id]


@app.patch("/shipment", response_model=Shipment)
def patch_shipment(
    id: int,
    # content: str | None = None,
    # weight: float | None = None,
    # status: str | None = None,
    shipment_update:ShipmentUpdate,
    session:SessionDep
) -> dict[str, Any]:
    # print("#"*15)
    # print(data)
    # print("#"*15)
    # print(data.model_dump(exclude_none=True))
    # print("#"*15)
    # shipment=shipments[id]
    # if content:
    #     shipment["content"]=content
    # if weight:
    #     shipment["weight"] = weight
    # if status:
    #     shipment["status"] = status
    
    # shipment.update(data.model_dump(exclude_none=True))
    # shipments[id]=shipment
    # return shipment
    # shipment = db.update(id,data)
    updated_data = shipment_update.model_dump(exclude_none=True)
    if not updated_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )
    shipment=session.get(Shipment, id)
    shipment.sqlmodel_update(updated_data)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment

@app.delete("/shipment")
def delete_shipment(id:int, session:SessionDep)->dict[str,str]:
    # shipments.pop(id)
    # db.delete(id)
    session.delete(session.get(Shipment,id))
    return {"detail": f"shipment is deleted with #{id}"}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )
