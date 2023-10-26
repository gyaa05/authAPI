from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_handler import sign_jwt
from descriptions.organisation import *
from models.db_session import get_session
from pydantic_models.all import UniversalyModel
from utils.password import hash_password
from models.organisation_cred import OrganisationCred


router = APIRouter()


@router.post("/register", summary="Register organisation", operation_id="register organisation",
             description=register_organisation_description)
async def register_user(register: UniversalyModel, session: AsyncSession = Depends(get_session)):
    organisation = OrganisationCred(login=register.login, password=hash_password(register.password))
    organisation.save(session)
    return {"token": sign_jwt("organisation_id", organisation.id, "organisation", 2592000)}


@router.post("/login", summary="Login organisation", operation_id="login-organisation",
             description=login_organisation_description)
async def login_user(login: UniversalyModel, session: AsyncSession = Depends(get_session)):
    organisation_cred = await OrganisationCred.get_by_login(login.login, session)
    if organisation_cred and organisation_cred.password == hash_password(login.password):
        return {"token": sign_jwt("organisation_id", organisation_cred.user_id, "organisation", 2592000)}
    return Response(status_code=403)
