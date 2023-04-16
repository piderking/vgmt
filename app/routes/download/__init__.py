from fastapi import APIRouter, Response
from ..responses import ExceptionResponse, DataResponse, UserDataResponse, DailyDataResponse
# from .fetch import fetch, fetchUser
from ...util import config


DownloadRouter = APIRouter(
    prefix="/download"
)

@DownloadRouter.get("/")
def Root() -> ExceptionResponse:
    return ExceptionResponse(
        message="Data Not Found",
        description="No data present with URL provided",
        help="https://" + config.doc_url + "/docs/api/download"
)

@DownloadRouter.get("/{user}/{date}")
@DownloadRouter.get("/{user}/daily/{date}")
def Get_Daily_Data(user:str, date:str) -> DailyDataResponse:
    """Get Daily Data

    Args:
        user (str): username
        date (str): month.day.year

    Returns:
        DailyDataResponse: Data formated into tight pydantic model
    """
    #fetch(user, date, type="day")
    return DailyDataResponse(
        data=["d", "d"],
        type="clean"
    )

@DownloadRouter.get("/{user}/weekly/{start_date}")
def Get_Weekly_Data(user, start_date) -> DailyDataResponse:
    """Get a weeks data

    Args:
        user (str): username
        start_date (str): month.day.year

    Returns:
        WeeklyDataResponse: Data formated into tight pydantic model course of a week
    """
    # fetch(user, start_date, type="week")
    return DailyDataResponse(
        data=["d", "d"],
        type="clean"
    )

@DownloadRouter.get("/{user}")
def Get_User_Data(user) -> DailyDataResponse:
    """Get a users data

    Args:
        user (str): _description_
    Returns:
        UserDataResponse: _description_
    """
    # fetchUser(user)
    return UserDataResponse(
        data=["d", "d"],
        type="clean"
    )