from fastapi import APIRouter
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import Any
from app.database.models import Shipment
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentStatus
from app.database.session import SessionDep


router = APIRouter()


@router.get("/shipment", response_model=Shipment)
async def get_shipment_list(id: int | None = None, session: SessionDep=None):
    shipment= await session.get(Shipment, id)
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


@router.post("/shipment")
async def create_shipment(shipment: ShipmentCreate, session:SessionDep) -> dict[str,int]:
    
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
    await session.commit()
    await session.refresh(new_shipment)
    return {"id":new_shipment.id}


# @app.put("/shipment")
# def shipment_update(
#     id: int, content: str, weight: float, status: str
# ) -> dict[str, Any]:
#     shipments[id] = {"content": content, "weight": weight, "status": status}
#     return shipments[id]


@router.patch("/shipment", response_model=Shipment)
async def patch_shipment(
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
    shipment=await session.get(Shipment, id)
    shipment.sqlmodel_update(updated_data)
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)

    return shipment

@router.delete("/shipment")
async def delete_shipment(id:int, session:SessionDep)->dict[str,str]:
    # shipments.pop(id)
    # db.delete(id)
    await session.delete(await session.get(Shipment,id))
    return {"detail": f"shipment is deleted with #{id}"}