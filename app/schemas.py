from enum import Enum
from pydantic import BaseModel,Field
from random import randint
class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
def get_random_destination():
    return randint(10000,99999)
class BaseShipment(BaseModel):
    content: str=Field(max_length=30)
    weight: float = Field(le=25,ge=1)
    # destination: int

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    content: str|None=Field(default=None,max_length=30)
    weight: float|None = Field(default=None,le=25,ge=1)
    destination: int|None = Field(default=None)
    status: ShipmentStatus