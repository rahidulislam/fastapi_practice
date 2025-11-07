from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.notification import NotificationService


class ShipmentEventService(BaseService):
    def __init__(self, session: AsyncSession,tasks):
        super().__init__(ShipmentEvent, session)
        self.notification_service = NotificationService(tasks)

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
        await self._notify(shipment, status)
        return await self._add(new_event)

    async def get_latest_item(self, shipment: Shipment):
        timeline = shipment.timeline
        timeline.sort(key=lambda event: event.created_at)
        print(timeline)
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

    async def _notify(self, shipment: Shipment, status:ShipmentStatus):
        match status:
            case ShipmentStatus.placed:
                await self.notification_service.send_templated_email(
                    subject="Your Order is Shipped",
                    recipients=[shipment.client_contact_email],
                    context={
                        "seller": shipment.seller.name,
                        "partner": shipment.delivery_partner.name,
                    },
                    template_name="mail_placed.html",
                )

                await self.notification_service.send_email(
                    subject="Shipment Placed",
                    recipients = [shipment.client_contact_email],
                    body=f"Your order with {shipment.seller.name} is picked up by {shipment.delivery_partner.name} and is on its way.",
                )
            case ShipmentStatus.out_for_delivery:
                await self.notification_service.send_email(
                    subject="Shipment is out for delivery",
                    recipients = [shipment.client_contact_email],
                    body=f"Your order is out for delivery by {shipment.delivery_partner.name}.",
                )
