from ..util import Thread
from ..util.debug import debug
from .server import DexcomOAuthServer
import math
from flask import abort
import requests
from ..util.csv import arrayToCsv
from typing import Any
from uuid import uuid4
class InvalidToken(Exception):
    """## Invalid Token Exception
        Used to catch when the token doesn't work from the server to the worker class
        ```python
        try:
            worker.getData()
        except InvalidToken as e:
            # Refresh Token
            # Wait on token to be aquired
    """

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        debug("Token is invalid! Try refreshing or recieving in the first place", type="error")
        return super().__call__(*args, **kwds)
class InvalidRequestType(Exception):
    """## Invalid Token Exception
        Used to catch when the token doesn't work from the server to the worker class
        ```python
        try:
            worker.getData()
        except InvalidToken as e:
            # Refresh Token
            # Wait on token to be aquired
    """

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        debug("Invalid Request Type at", type="error")
        return super().__call__(*args, **kwds)

class DexcomWebWorker(Thread):
    """Threaded Fetching System, based on util.thread.Thread

    Raises:
        InvalidToken: Catcher for oauth.server.OAuthSever
        Warning: General Warning or Error

    """
    # NOTE self.data is in the webworker thread, self.data is the requests
    def __init__(self) -> None:
        self.total_blood_sugar = 0
        self.total_entries = 0
        self._token = None

        super().__init__(self_start=False)

    @property
    def token(self):
        if self._token is None:
            raise InvalidToken("Token passed through to DexcomWebWorker is None!")
        return self._token # TODO Make sure up to dates

    def getData(self, _type: str, year: str, month: str, day:str or None=None, asCsv: bool = True)->list:
        """Wrapper Function

        Args:
            _type (str): _description_
            year (str): _description_
            month (str): _description_
            day (str, optional): _description_. Defaults to "01".
            asCsv (bool, optional): _description_. Defaults to True.
        """
        uuid = uuid4()
        self.data.append({"type":_type, "id":uuid, "year": year, "month":month, "day":None, "asCsv": asCsv})
        yield uuid
        while True:
            for count, result in enumerate(self.unsorted_results):
                if result["id"] == uuid:
                    self.data.pop(count) # NOTE Hopefully this doesn't cause problems when multiple getData threads are running
                    yield result["data"]

    def fcn(self, index: int, data: dict):
        """Runner Funtion for this Thread

        Args:
            index (int): Provideded by Program (index in target)
            data (dict): Provided by Program (data)
            ```python
            Data: {"id", "url", "year", "month", "day"}
            Results: [{"id": UUID4, "data":{"url", "year", "month", "day"}}]
            ```

        Raises:
            InvalidRequestType: Data object requires "type" is request raise that warning

        Returns:
            list: Will be appended to self.results
        """
        if data["type"] == "month":
            # Fetch Month Data (in-thread configuration)
            return [{"id": data["id"], "data": self.requestData(data["url"], data["year"],data["month"], asList=True)}]
        elif data["type"] == "day":
            # Fetch Day Data (in-thread configuration)
            if data["day"] is None:
                raise InvalidRequestType("No date specified for request type of Day Data")
            return [{"id": data["id"], "data":self.requestDayData(data["url"], data["year"],data["month"], data["day"], asList=True)}]


        raise InvalidRequestType("Type of Data to fetch isn't specified")
    def requestDayData(self, url: str, year: str, month: str, day:str, asList: bool = False, asCsv:bool = False) -> None or list or Any:

        _year, _month, _day = (int(year), int(month), int(day)) # Ensure Integers


        max_day_value = 1

            # Get Max value for a day in given month
        if _month == 1 or _month == 3 or _month == 5 or _month == 7 or _month == 8 or _month == 10 or _month == 12:
            max_day_value = 31
        elif _month == 4 or _month == 6 or _month == 9 or _month == 11:
            max_day_value = 30
        elif _year % 4 == 0:
            max_day_value = 28
        else:
            max_day_value = 28

        if len(month) != 1 and len(month) != 2: # Neither 1 nor 2 in lengt
            abort(400)
        # Next Day
        next_day = str(_day+1)

        # Max Sure format 01
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        if len(next_day) == 1:
            next_day = "0" + next_day

        if _day > max_day_value or _day + 1 > max_day_value:
            raise Exception("Day is to large, request {}/{}/{}, max is {}/{}/{}".format(month, day, year, month, max_day_value, year))

        query = {
            "startDate": "{}-{}-{}T00:00:00".format(year, month, day),
            "endDate": "{}-{}-{}T23:59:59".format(year, month, next_day)
        }
        headers = {"Authorization": "Bearer {}".format(self.token)}

        response = requests.get(url, headers=headers, params=query)

        if len(response.content) == 0: # Invalid Token
            raise InvalidToken()



        if asList or asCsv:
            # Get it returned as a list
            tList = []
            for i in reversed(response.json()["records"]):
                # Reverse List (Bottom Timestamp is the Lowest)
                tList.append([i["systemTime"], i["value"], i["trendRate"]])
            if asCsv:
                arrayToCsv(year, month, day, self.token, tList)

            return tList # Return the tList response as data
        return response

    def requestData(self, url:str, year: str, month: str, asList: bool = False, asCsv: bool = False):

        _year, _month = (int(year), int(month)) # Ensure Integers


        max_day_value = "01"

            # Get Max value for a day in given month
        if _month == 1 or _month == 3 or _month == 5 or _month == 7 or _month == 8 or _month == 10 or _month == 12:
            max_day_value = "31"
        elif _month == 4 or _month == 6 or _month == 9 or _month == 11:
            max_day_value = "30"
        elif _year % 4 == 0:
            max_day_value = "28"
        else:
            max_day_value = "28"

        if len(month) != 1 and len(month) != 2: # Neither 1 nor 2 in lengt
            abort(400)

        if len(month) == 1:
            month = "0" + month



        query = {
            "startDate": "{}-{}-01T00:00:00".format(year, month),
            "endDate": "{}-{}-{}T23:59:59".format(year, month, max_day_value)
        }

        headers = {"Authorization": "Bearer {}".format(self.token)}

        response = requests.get(url, headers=headers, params=query)

        if len(response.content) == 0 or response.content == b'':
            raise Exception("Token Invalid, try /erase and restarting it") # Make Custom Exception

        if len(response.content) == 0: # Invalid Token
            raise InvalidToken()




        if asList or asCsv:
            tList = []
            for i in reversed(response.json()["records"]):
                # Reverse List (Bottom Timestamp is the Lowest)
                tList.append([i["systemTime"], i["value"], i["trendRate"]])

            if asCsv:
                arrayToCsv(year, month, "01-{}".format(max_day_value), self.token, tList)

            return tList # Return the tList response as data
        return response

class DexcomWorker(Thread):

    def __init__(self,) -> None:
        self.unsorted_data = []
        self.total_blood_sugar = 0
        self.total_entries = 0
        self.web_worker = DexcomWebWorker()

        super().__init__(self_start=False)

    def start(self) -> None:
        debug("Starting Dexcom Worker Thread", type="info")
        self.web_worker.start()
        return super().start()

    def fcn(self, index: int, data:list):
        """Multi-Thread Functionality

        Args:
            index (int): What index in the target it's at
            data (list): Blood Sugar Entries

        Returns:
            _type_: _description_
        """
        for d in data:
            self.total_blood_sugar += int(d[1])
            self.total_entries += 1
        return [data]

