from fastapi import APIRouter, FastAPI
from .download import DownloadRouter
def useRouter(app: FastAPI,router:APIRouter):
    app.include_router(router)

base = APIRouter(
    prefix="/api"
)
