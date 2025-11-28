from uuid import UUID
from fastapi import APIRouter, Request
from fastapi import HTTPException, status
from typing import Any

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.dependencies import DeliveryPartnerServiceDep, SellerDep, ServiceDep
from app.database.models import Shipment
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentRead
from app.utils import TEMPLATE_DIR


router = APIRouter(prefix="/shipment", tags=["Shipment"])
templates = Jinja2Templates(TEMPLATE_DIR)

@router.get("/", response_model=ShipmentRead)
async def get_shipment_list(id: UUID, service: ServiceDep):
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment is not found"
        )
    return shipment

@router.get("/track")
async def get_tracking(request:Request,id:UUID, service:ServiceDep):
    shipment = await service.get(id)
    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline
    # return HTMLResponse(content=f"<body><h1>Tracking Info for Shipment {id}</h1><p>Status: {shipment.status}</p></body>", status_code=200)
    return templates.TemplateResponse(request,"track.html", context)

@router.post("/", response_model=ShipmentRead)
async def create_shipment(
    shipment: ShipmentCreate, service: ServiceDep, seller: SellerDep
) -> Shipment:
    return await service.add(shipment, seller)


@router.patch("/", response_model=ShipmentRead)
async def patch_shipment(
    id: UUID, shipment_update: ShipmentUpdate, service: ServiceDep, partner: DeliveryPartnerServiceDep
) -> dict[str, Any]:
    updated_data = shipment_update.model_dump(exclude_none=True)
    if not updated_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )
    shipment = await service.update(id, updated_data, partner)

    return shipment


@router.delete("/")
async def delete_shipment(id: UUID, service: ServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"shipment is deleted with #{id}"}
