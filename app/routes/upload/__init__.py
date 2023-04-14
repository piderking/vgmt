from fastapi import APIRouter, Response
from ..responses import ExceptionResponse, DataResponse, UserDataResponse, DailyDataResponse


url = "https://google.com"
DownloadRouter = APIRouter(
    prefix="/download"
)