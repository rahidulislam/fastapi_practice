from fastapi import APIRouter
from fastapi import HTTPException, status
from typing import Any
from app.api.dependencies import ServiceDep
from app.database.models import Shipment
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentRead


router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment_list(id: int, service: ServiceDep):
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment is not found"
        )
    return shipment


@router.post("/", response_model=ShipmentRead)
async def create_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    return await service.add(shipment)


@router.patch("/", response_model=ShipmentRead)
async def patch_shipment(
    id: int, shipment_update: ShipmentUpdate, service: ServiceDep
) -> dict[str, Any]:
    updated_data = shipment_update.model_dump(exclude_none=True)
    if not updated_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )
    shipment = await service.update(id, updated_data)

    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"shipment is deleted with #{id}"}
