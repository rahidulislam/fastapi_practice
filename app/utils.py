
from pathlib import Path
from fastapi import HTTPException, status
import jwt
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from app.config import security_settings

APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR / "templates"
def generate_access_token(data:dict, expiry:timedelta=timedelta(days=1))->str:
    return jwt.encode(
            payload={
                **data,
                "jti": str(uuid4()),
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