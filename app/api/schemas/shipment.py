from datetime import datetime
from sqlmodel import Field, SQLModel
from app.database.models import ShipmentStatus

# def get_random_destination():
#     return randint(10000, 99999)


class BaseShipment(SQLModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int


class ShipmentRead(BaseShipment, table=True):
    # __tablename__ = "shipment"
    id: int = Field(default=None, primary_key=True)
    status: ShipmentStatus
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(SQLModel):
    content: str | None = Field(default=None, max_length=30)
    weight: float | None = Field(default=None, le=25, ge=1)
    destination: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
