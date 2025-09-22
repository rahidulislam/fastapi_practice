from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class ShipmentEventService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(ShipmentEvent, session)

    async def add(
        self,
        location: int,
        shipment: Shipment,
        status: ShipmentStatus = None,
        description: str = None,
    ) -> ShipmentEvent:
        if not location or not status:
            last_location = await self.get_latest_item(shipment)
            location = location if location else last_location.location
            status = status if status else last_location.status
        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=description
            if description
            else self._generate_description(status, location),
            shipment_id=shipment.id,
        )
        return await self._add(new_event)

    async def get_latest_item(self, shipment: Shipment):
        timeline = shipment.timeline
        timeline.sort(key=lambda event: event.created_at)
        return timeline[-1]

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned to delivery partner."
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.delivered:
                return "shipment delivered"
            case _:
                return f"scanned at {location}"
