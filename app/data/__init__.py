from .structure import DailyDataModel, DataModel, UserDataModel, WeeklyDataModel
from fastapi import APIRouter



dexcom = APIRouter(prefix="/dexcom")

@dexcom.get("/")
def dexcom_root():
    return