import os
from ..config import DATA_PATH
from ..util.debug import debug
def arrayToCsv(year: str, month: str, date: str, token: str, data: list):
    """Convert a list of data into a CSV file

    Args:
        year (str): Year of Data
        month (str): Month of Data
        date (str): Date of Data
        token (str): Token
    """
    if type(token) is not str or len(token) < 8: # TODO Find token length for here
        raise TypeError("Argument: Token, cannot be None type.")

    directory = os.path.join(DATA_PATH, token[:8])
    if not os.path.exists(os.path.join(directory)): # Create a oath
        os.makedirs(directory)

    path = os.path.join(directory, "{}-{}-{}.csv".format(month, date, year))
    if os.path.exists(path):
        debug("Data File at {} already exsists, overwriting".format(path),type="warn")
        os.remove(path)

    with open(path, "a") as f:
        f.write("System Time,Value,Trend Rate")

        for row in data:
            f.write("\n{},{},{}".format(row[0], row[1],row[2])) # Append to File

        debug("Finished Writing Datafile at {}".format(path), type="sucess")
        f.close()