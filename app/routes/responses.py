from pydantic import BaseModel
from ..data import DailyDataModel, DataModel, UserDataModel, WeeklyDataModel

class ExceptionResponse(BaseModel):
    message: str # Heh
    description: str | None = None
    help: str = "Exception in Request"

class DataResponse(BaseModel):
    data: DataModel
    type: str = "any"
    help: str = "Data Response; for structure visit @data/structure.py"

class DailyDataResponse(DataResponse):
    data: DailyDataModel
    type = "daily"
class WeeklyDataResponse(DataResponse):
    data:  WeeklyDataModel
    type = "daily"
class UserDataResponse(DataResponse):
    data: UserDataModel
    type = "user"


    
