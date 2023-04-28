from fastapi import APIRouter, FastAPI,Header, Depends,HTTPException
from .download import DownloadRouter
from typing import Annotated




async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


base = APIRouter(
    prefix="/api",
    dependencies=[Depends(verify_token), Depends(verify_key)]
)




@base.get("/items/")
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]