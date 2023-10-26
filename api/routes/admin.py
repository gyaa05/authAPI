from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_handler import sign_jwt
from descriptions.admin import *
from models.db_session import get_session
from utils.password import hash_password
from pydantic_models.all import UniversalyModel
from models.admin_cred import AdminCred


router = APIRouter()


@router.post("/register", summary="Register admin", operation_id="register-admin",
             description=register_admin_description)
async def register_admin(register: UniversalyModel, session: AsyncSession = Depends(get_session)):
    admin = AdminCred(login=register.login, password=hash_password(register.password))
    admin.save(session)
    return {"token": sign_jwt("admin_id", admin.id, "admin", 2592000)}


@router.post("/login", summary="Login admin", operation_id="login-admin",
             description=login_admin_description)
async def login_admin(login: UniversalyModel, session: AsyncSession = Depends(get_session)):
    admin = await AdminCred.get_by_login(login.login, session)
    if admin and admin.password == hash_password(login.password):
        return {"token": sign_jwt("admin_id", admin.id, "admin",
                                  2592000)}
    return Response(status_code=403)
