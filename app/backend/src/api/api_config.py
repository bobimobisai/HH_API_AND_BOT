from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles
from backend.src.api.v1.routers.router_base import BaseRouter
from backend.src.api.v1.routers.router_auth import AuthRouter


APP = FastAPI()


APP.mount("/static", StaticFiles(directory="backend/src/static"), name="static")
APP.include_router(BaseRouter)
APP.include_router(AuthRouter)
