'''
 # @ Author: Peter Bowman
 # @ Create Time: 2023-03-09 18:38:36
 # @ Modified by: Peter Bowman
 # @ Modified time: 2023-03-09 18:38:47
 # @ Description: Data Structure
 '''

from pydantic import BaseModel
# from numpy import ndarray

class DataModel(BaseModel):
    @classmethod
    def from_raw(cls, data:dict) -> any:
        """
        New Class from raw dict with class attributes
        .from_raw({"dataset_id":"id"}) -- must correspond with type of class
        """
        nDataModel = cls # Set atrs
        for atr in data: # Loop through attributes and set them 
            setattr(nDataModel, atr, data[atr])
            #print(data[atr])
        return nDataModel # Return created model
    """
    Raw Structure for Dataset in VGM
    """
    dataset_id: str # UserID
    date_created: str # Date of creation
class UserDataModel(DataModel):

    """Raw Data Structure for building files or decoding files
    """
    user_id: str # uuid:str; UUID Generated for User
    gender:str # male, female, other
    age:int # 0-100 age

class FiveMinuteDataModel(DataModel):
    """User's Data; in five minute increaments
    Smallest unit; measurement built in
    """

    time_stamp: str # Timestamd (Unused in model, used is sorting though)
    glucose: int # Glucose at the time
    heart_rate: int # Heart Rate
    exercise_intensity: float # Percent 0-1, ex: 0 means no excersise, 1 means maxing out...
    stress_intensity: float # Number between 0 - 1; how much higher stress is than (longer sustained abnormal high heart rates with patern)


class DailyDataModel(DataModel):
    """480 Five Minute Data Models
    For training different types of models
    NOT FOR USE RECURSIVELY 
    """
    date: str
    time_stamp: str
    measurements: list[FiveMinuteDataModel] # 480 Data Models

class WeeklyDataModel(DataModel):
    """480 Five Minute Data Models
    """
    date: str
    time_stamp: str
    measurements: list[FiveMinuteDataModel] # 480 Data Models

