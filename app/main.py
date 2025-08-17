from fastapi import FastAPI, HTTPException, status
from typing import Any
from scalar_fastapi import get_scalar_api_reference
from app.schemas import ShipmentRead,ShipmentCreate,ShipmentUpdate,ShipmentStatus
from app.database import Database

app = FastAPI()
db= Database()

# shipments = {
#     1: {"content": "Books", "weight": 3, "status": "in_transit","destination": 1234},
#     2: {"content": "Electronics", "weight": 5, "status": "delivered", "destination": 1234},
#     3: {"content": "Clothes", "weight": 2, "status": "placed", "destination": 1234},
#     4: {"content": "Furniture", "weight": 15, "status": "delivered", "destination": 1234},
#     5: {"content": "Toys", "weight": 4, "status": "out_for_delivery", "destination": 1234},
# }


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment_list(id: int | None = None):
    shipment= db.get(id)
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
def create_shipment(shipment: ShipmentCreate) -> dict[str,int]:
    
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
    new_id = db.create(shipment)
    return {"id":new_id}


# @app.put("/shipment")
# def shipment_update(
#     id: int, content: str, weight: float, status: str
# ) -> dict[str, Any]:
#     shipments[id] = {"content": content, "weight": weight, "status": status}
#     return shipments[id]


@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(
    id: int,
    # content: str | None = None,
    # weight: float | None = None,
    # status: str | None = None,
    data:ShipmentUpdate
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
    shipment = db.update(id,data)
    return shipment

@app.delete("/shipment")
def delete_shipment(id:int)->dict[str,str]:
    # shipments.pop(id)
    db.delete(id)
    return {"detail": f"shipment is deleted with #{id}"}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )
