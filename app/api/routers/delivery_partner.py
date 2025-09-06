from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas.delivery_partner import DeliveryPartnerCreate, DeliveryPartnerRead, DeliveryPartnerUpdate
from app.api.dependencies import SellerServiceDep, get_partner_access_token, DeliveryPartnerDep
from app.core.security import oauth2_scheme
from app.database.models import Seller
from app.database.redis import add_jti_to_blacklist
from app.database.session import SessionDep
from app.utils import decode_access_token

router = APIRouter(prefix="/partner", tags=["Partner"])

# Register Delivery Partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(seller: DeliveryPartnerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }
@router.put("/")
async def update_delivery_partner(update_partner:DeliveryPartnerUpdate, partner:DeliveryPartnerDep, service):
    pass

@router.get("/logout")
async def logout_delivery_partner(token_data:Annotated[dict,Depends(get_partner_access_token)]):
    await add_jti_to_blacklist(token_data['jti'])
    return {"detail": "Logout successful"}