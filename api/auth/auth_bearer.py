from pydantic import BaseModel

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.auth_handler import decode_jwt


class JWTHeader(BaseModel):
    user_id: int | None = None
    deliveryman_id: int | None = None
    expires: float
    admin: bool = False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, admin: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.admin = admin

    async def __call__(self, request: Request) -> JWTHeader:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        # Смотрим, есть ли Authorization
        if credentials:
            if not credentials.scheme == "Bearer":
                # Нет Bearer
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            # расшифровываем JWT
            decoded = self.verify_jwt(credentials.credentials)
            if not decoded:
                # Если ничего нет, то возвращаем 403
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            header: JWTHeader = JWTHeader(**decoded)
            return header
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwt_token: str):
        payload = decode_jwt(jwt_token)
        return payload if payload else None
