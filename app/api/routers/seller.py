from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas.seller import SellerCreate, SellerRead
from app.api.dependencies import SellerServiceDep, get_seller_access_token
from app.core.security import oauth2_scheme_seller as oauth2_scheme
from app.database.models import Seller
from app.database.redis import add_jti_to_blacklist
from app.database.session import SessionDep
from app.utils import decode_access_token

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }
@router.get("/dashboard")
async def get_dashboard(token:Annotated[str, Depends(oauth2_scheme)], session:SessionDep)->Seller:
    data= decode_access_token(token)
    if data is None:
        return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or expired",
            )
    seller = await session.get(Seller, data["user"]["id"])
    return seller

@router.get("/logout")
async def logout_seller(token_data:Annotated[dict,Depends(get_seller_access_token)]):
    await add_jti_to_blacklist(token_data['jti'])
    return {"detail": "Logout successful"}
