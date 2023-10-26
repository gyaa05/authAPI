import logging

from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from routes import admin

from routes import organisation

from models.db_session import global_init, create_session

description = """
Deliveryman register request require a header in the following format: {'Authorization': 'Bearer jwt_token'}
In JWT payload should be deliveryman_id or user_id
JWT Payload structure:
    deliveryman_id: int | None (id of deliveryman from DB)
    expires: float (the expiration time of the JWT)
    admin: bool (used for certain endpoints that are for admins)

Other requests don't need authorization
"""

app = FastAPI(title="Market Auth API", description=description)
app.include_router(organisation.router, prefix="/organisation", tags=["organisation"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    async with create_session() as sess:
        request.state.session = sess
        response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.on_event('startup')
async def startup_event():
    await global_init()
