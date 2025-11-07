from datetime import datetime
from datetime import timedelta
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import DeliveryPartner, Seller, Shipment, ShipmentStatus
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService
from app.services.shipment_event import ShipmentEventService


class ShipmentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService,
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service

    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now()
            + timedelta(days=3),  # Example estimated delivery
            seller_id=seller.id,
        )
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        shipment = await self._add(new_shipment)
        await self.event_service.add(
            shipment=shipment,
            location=seller.zip_code,
            status=ShipmentStatus.placed,
            description=f"assigned to {partner.name} for delivery",
        )
        return shipment

    async def update(
        self, id, shipment_update: ShipmentUpdate, partner: DeliveryPartner) -> Shipment:
        shipment = await self.get(id)
        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this shipment",
            )
        update = shipment.sqlmodel_update(shipment_update)
        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery
        if len(update) > 1 or not shipment_update.estimated_delivery:
            self.event_service.add(shipment=shipment, **update)
        return await self._update(shipment)

    async def delete(self, id: int) -> None:
        self._delete(await self.get(id))
