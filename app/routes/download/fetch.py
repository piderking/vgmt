'''
 # @ Author: Peter Bowman
 # @ Create Time: 2023-03-09 16:45:29
 # @ Modified by: Peter Bowman
 # @ Modified time: 2023-03-09 16:45:55
 # @ Description: Fetch from storage bucket
 '''
#TODO Make Fetching Async

from ...data import DailyDataModel, WeeklyDataModel, UserDataModel
#from ...firebase import fireapp, bucket
from ...util import config
from uuid import uuid4
import os
from firebase_admin import storage



# Create Firbase Bucket
bucket = storage.bucket()


# from firebase_admin.storage import Ex
class Blob(object):
    def __init__(self, file_source:str, store_in_mem: bool = True, csv_path: str = os.path.abspath("./data"), filename:str | None = None) -> None:
        """Creates a blob utility class; 

        Args:
            file_source (str): file looking to download; ex: "default.txt" (include .csv)
            store_in_mem (bool) if string should be stored in memory (dev/parsing) or locally stored on site (prod) then brought into memory
            csv_path (str, optional): path csv files are stored; if they are being stored.
        """
        self.file_source: str = file_source
        self.store_in_mem: bool = store_in_mem
        self.csv_path: None | str = csv_path
        # Set the FilePath either to the filename or firesource depending on what is passed
        self.filename = filename if filename is not None else file_source
        self.path = os.path.join(csv_path, file_source) if filename is None else os.path.join(csv_path, filename)
        self.data = None
        # self.data will either be a string; or a filepath (depending if self.file)
    @classmethod
    def downloadBlob(cls, file_source:str, store_in_mem: bool = True, csv_path:str=os.path.abspath("./data"), filename:str | None = None,) -> str:
        """Download Data from Google Cloud Storage Bucket

        Args:
            file_source (str): file looking to download; ex: "default.txt" (include .csv)
            store_in_mem (bool) if string should be stored in memory (dev/parsing) or locally stored on site (prod) then brought into memory
            csv_path (str, optional): path to csv directory, filename is same as downloaded unless specified
        
        Returns:
            Either csv data; in text form or file path
            csv

        Testing:
            Store in Memory: ✅
            Store on disk:✅
            Memory Buffer: tbd
        """
        if store_in_mem:
            # Simply better
            return bucket.blob(file_source).download_as_string()
        
        # Downloading the file to memory; else download it to a file and (it should retain its filename)
        # TODO If this errors its probally because of save location being messed up
        if not store_in_mem and os.path.exists(os.path.join(csv_path, filename)): # file name prior set to eitiher source or custom so we only need to check once
            tid = str(uuid4()) # If name is occupied
            return bucket.blob(file_source).download_to_filename(os.path.join(csv_path, tid)),os.path.join(csv_path, tid)
        else:                 
            return bucket.blob(file_source).download_to_filename(os.path.join(csv_path, file_source if filename is None else filename)), os.path.join(csv_path, file_source if filename is None else filename) if not store_in_mem else None
            
      
                 
    def __call__(self, ) -> str or None:
        
        if self.store_in_mem:
            # Self.data = downloading the blob;
            self.data = self.downloadBlob(self.file_source, True, self.csv_path, self.fil)
            return self.data
        else: 
            self.downloadBlob(self.file_source, store_in_mem=False, csv_path=self.csv_path, filename=self.filename)
            return None

def download_to_mem(file_source_blob):
    Blob("default.txt", True)
# Download CSV Files to local directory


def download_blob(source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # Bucket already initalized from gcloud instance

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {}to local file {}.".format(
            source_blob_name,destination_file_name
        )
    )
#download_blob("default.txt", "default.txt")
def download(url:str):
    """Download Data Files from GCLOUD

    Args:
        url (str): _description_
    """
    return
def fetchUser(user:str):
    return 
def fetch(user:str, date:str, type:str) -> DailyDataModel | WeeklyDataModel | UserDataModel:
    """Fetch Date/Week of Data

    Args:
        user string: username
        date string: month.date.year
        type (str | None, optional): _description_. Defaults to None.

    Returns:
        DailyDataModel: _description_
    """


    return 