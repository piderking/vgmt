import os
from ..config import DATA_PATH
from ..util.debug import debug
import csv
from uuid import uuid4
from ..util.list import flatten
from .thread import Thread
import concurrent.futures
import numpy as np
def csvToArray(csvFilePath: str) -> list:
    """Transform a CSV File Path into an array (list)

    Args:
        csvFilePath (str): Path at which destinted CSV File can be found

    Raises:
        FileNotFoundError: No file at path specified was found

    Returns:
        list: array generated from inside of the CSV file
    """
    if not os.path.exists(csvfile):
        raise FileNotFoundError(str(csvFilePath) + " is not defined")
    with open(csvFilePath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ',) #  quotechar='|'
        for row in spamreader:
            print(', '.join(row))
        return [[x[0], int(x[1]), float(x[2])] for x in spamreader]

def step_range(lent:float, interval: float):
    count = 0
    while count < lent:

        if count > lent:
            break
        else:
            yield count, count + interval
        count += interval
    yield count, lent - 1
class CSV_Processor(Thread):
    def __init__(self, skips:list,file:str,  batch: int or None = None,  target: int = 3, self_start: bool = True, daemon: bool = True, data: list = ..., basis: float = 0.2, times: int = 3) -> None:
        self.skips = skips
        self.words=""
        self.file = open(file, "a")
        self.batch = batch

        if self.batch is None:
            self.batch = int(len(data) / 10)
        debug("Batch is at {}".format(self.batch))
        data = [data[f:s] for f, s in step_range(len(data), self.batch) ]

        if len(data) > 0:
            target = int(len(data) / 10)
        super().__init__(target, self_start, daemon, data, basis, times)
    def fcn(self, index: int = 0, d: list = [], skips: list = []) -> list:

        for data in d:
            f = []
            for count, item in enumerate(data):
                if not count in skips:
                    f.append(item)
            self.words += "" + ",".join(f) + "\n"

        return []
    def needsOpperation(self) -> bool:
       # debug("Processor at " + str(self.target))
        # print("Length of Data: " + str(len(self.data)) )
        #print("Length of Results: " + str(len(self.unsorted_results)) )
        return super().needsOpperation()

    def join(self) -> None:
        self.file.write(self.words)
        return super().join()
    def threaded(self: Thread, fcn):
        """ ## Threading Decorator
            Runs a paralized task for the amount in the target

        """
        def wrapper(*args, **kwargs):
            target = list(range(self.target)) # range(self.target if len(self.data)/self.target >= 1 else len(self.data))
            results = {}
            # We can use a with statement to ensure threads are cleaned up promptly
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(fcn, index=i, d=self.data[i], skips=self.skips): idx for idx,
                            i in enumerate(target)} # { Future: Submit}

                # Amount of Tasks
                tasks = len(futures)

                # Add to total running
                self.tasks += tasks
                self.total_tasks += tasks


                for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                    i = futures[future] # Future
                    try:
                        # store result
                        data = future.result()

                        # check to see if in array form
                        if len(data) == 1:
                            data = data[0]
                        results[i] = data

                        self.tasks -= 1
                    #except Exception as exc:
                    #    self.tasks -= 1
                    #    debug('{} generated an exception: {}'.format(
                    #       target[i], exc))
                    finally: pass

            # sort and put in array
            final = []
            for k, v in sorted(results.items()):
                final.append(v)
                self.unsorted_results.append(v)
            self.results.append(final)
            return final
        return wrapper
class CSV_Writer(Thread):
    def __init__(self, file:str, target: int = 5, batch: int = 1, self_start: bool = True, daemon: bool = True, data: list = ..., basis: float = 0.2, times: int = 3) -> None:
        self.file = open(file, "a")
        self.data=""
        self.batch = batch
        super().__init__(target=target, self_start=True, daemon=daemon, data=data, basis=basis, times=times)

    def needsOpperation(self) -> bool:
        print("Writer at " + str(self.target))
        return super().needsOpperation()
    def fcn(self, index: int = 0, d: list = [],) -> list:
        self.data += "" + ",".join(d) + "\n"
        return d

    def threaded(self: Thread, fcn):
        """ ## Threading Decorator
            Runs a paralized task for the amount in the target

        """
        def wrapper(*args, **kwargs):
            target = list(range(self.target)) # range(self.target if len(self.data)/self.target >= 1 else len(self.data))
            results = {}
            # We can use a with statement to ensure threads are cleaned up promptly
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(fcn, index=i, d=self.data[i]): idx for idx,
                            i in enumerate(target)} # { Future: Submit}

                # Amount of Tasks
                tasks = len(futures)

                # Add to total running
                self.tasks += tasks
                self.total_tasks += tasks


                for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                    i = futures[future] # Future
                    try:
                        # store result
                        data = future.result()

                        # check to see if in array form
                        if len(data) == 1:
                            data = data[0]
                        results[i] = data

                        self.tasks -= 1
                    #except Exception as exc:
                    #    self.tasks -= 1
                    #    debug('{} generated an exception: {}'.format(
                    #       target[i], exc))
                    finally: pass

            # sort and put in array
            final = []
            for k, v in sorted(results.items()):
                final.append(v)
                self.unsorted_results.append(v)
            self.results.append(final)

            return final
        return wrapper

# Incomplete
def combineCsvFiles(csvFilePaths: list[str]) -> str:
    # Final Filepath
    directory = os.path.join(os.path.abspath("."), "data", "f")
    if not os.path.exists(directory):
        os.makedirs(directory)

    new_path = os.path.join(directory, str(uuid4())+".csv")
    for path in csvFilePaths:
        if not os.path.exists(path):
            #debug("Data File at {} already exsists, overwriting".format(path),type="warn")
            raise FileNotFoundError("File at doesn't exsist, path: {}".format(path))

    files = [open(fpath, "r").read().split("\n") for fpath in csvFilePaths]
    files = [[entries.split(",") for entries in text] for text in files]
    """

    [
        [
            "sdfsdf,sdfsdf", "sdfsedf,sdfsdf", "sdfsdf"
        ],[
            "sdfsdf", "sdfsedf", "sdfsdf"
        ],
    ]

    """
    #print([text for text in files][0][0].split(","))

    _headers = flatten([text[0] for text in files]) # Flatten Array. Includes doubles
    headers = [] #
    skip = [] # Skip the column
    for count, header in enumerate(_headers):
        if not header in headers and not header == "":
            headers.append(header)
        else:
            skip.append(count)
    # debug("Headers are {}, skips are {}".format(str(headers), str(skip)))
    # Flatten all the files (Single List)

    #files = [file[1:] for file in files] # Remove headers


    with open(new_path, "a") as f:
        lines = [[] for x in range(len(files[0]))]  # Use header as headers for item length
        print(len(lines))
        # Flatten but keep linal structure
        for file in files:
            for line_number, line in enumerate(file):
                #print(len(file), line_number)
                if line_number == len(file) :
                    continue
                lines[line_number].extend(line)
        del files

        worker = CSV_Processor(skip, new_path, data=lines)

        try:
            while len(worker.data) > 0:
                # print(len(worker.data))
                pass
        except KeyboardInterrupt:
            pass

        worker.join()



        debug("Finished Writing Datafile at {}".format(new_path), type="sucess")
        f.close()

def arrayToCsv(year: str, month: str, date: str, token: str, data: list, t:str = "bs", ) -> str:
    """Convert a list of data into a CSV file

    Args:
        year (str): Year of Data
        month (str): Month of Data
        date (str): Date of Data
        token (str): Token
        t (str): type of data, "bs", "hr", "f", "ts"
    Returns:
        str: Filepath
    """
    headers = {
        "bs": "System Time,Time Stamp,Value,Trend Rate", # Blood Sugar
        "hr": "", # Heart Rate
        "f": "", # Final (Blood Sugar and Heart Rate)
        "c":"System Time,Time Stamp,Carbs,Insulin Carb Ratio,IOB, Value",
        "t": "" # Testing Data
    }
    if type(token) is not str or len(token) < 8: # TODO Find token length for here
        raise TypeError("Argument: Token, cannot be None type.")
    if not t in headers.keys():
        raise KeyError("Target Header passed doesn't exsist")
    directory = os.path.join(DATA_PATH, t, token[:8])
    if not os.path.exists(os.path.join(directory)): # Create a oath
        os.makedirs(directory)
    path = os.path.join(directory, "{}-{}-{}.csv".format(month, date, year))
    if os.path.exists(path):
        debug("Data File at {} already exsists, overwriting".format(path),type="warn")
        os.remove(path)

    with open(path, "a") as f:
        f.write(headers[t])

        amt = headers[t].split(",")[:-1]
        for rc, row in enumerate(data):
            line = "\n"
            # f.write()) Time Values, requries Time Stamps
            for count, col in enumerate(row):
                if amt[count] == "Time Stamp":
                    # debug("Here!", type="error")
                    line += str(rc)
                    line+=","

                line += str(col)
                line+=","

            f.write(line)
        debug("Finished Writing Datafile at {}".format(path), type="sucess")
        f.close()

    return path