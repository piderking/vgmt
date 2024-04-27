import os
from ..config import DATA_PATH
from ..util.debug import debug
import csv


def csvToArray(csvFilePath) -> list:
    with open('eggs.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ',) #  quotechar='|'
        for row in spamreader:
            print(', '.join(row))
        return [[x[0], int(x[1]), float(x[2])] for x in spamreader]
def arrayToCsv(year: str, month: str, date: str, token: str, data: list, t:str = "bs", ):
    """Convert a list of data into a CSV file

    Args:
        year (str): Year of Data
        month (str): Month of Data
        date (str): Date of Data
        token (str): Token
        t (str): type of data, "bs", "hr", "f", "ts"
    """
    headers = {
        "bs": "System Time,Time Stamp, Value,Trend Rate", # Blood Sugar
        "hr": "", # Heart Rate
        "f": "", # Final (Blood Sugar and Heart Rate)
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

        amt = headers[t].split(",")
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