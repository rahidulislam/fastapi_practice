from time import timezone
from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta
from app.config import security_settings

def generate_access_token(data:dict, expiry:timedelta=timedelta(days=1))->str:
    return jwt.encode(
            payload={
                **data,
                "exp": datetime.now(timezone.utc) + expiry,
            },
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET,
        )

def decode_access_token(token:str)->dict:
    try:
        return jwt.decode(
            jwt=token,
            algorithms=[security_settings.JWT_ALGORITHM],
            key=security_settings.JWT_SECRET,
        )
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Token has expired") from err
    except jwt.PyJWTError:
        return None