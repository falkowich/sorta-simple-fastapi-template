import logging

from fastapi import Depends, FastAPI

from app.api import auth, ping, users
from app.core import get_current_active_user
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(
        ping.router, dependencies=[Depends(get_current_active_user)]
    )
    application.include_router(
        users.router,
        prefix="/users",
        tags=["users"],
        dependencies=[Depends(get_current_active_user)],
    )
    application.include_router(auth.router, tags=["auth"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down")
