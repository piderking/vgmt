from ..util.csv import arrayToCsv
def generate_faux_insulin(toCsv:bool = False) -> list:
    """System Time,Time Stamp,Carbs,Insulin Carb Ratio,IOB, Value

    Returns:
        list: System Time,Time Stamp,Carbs,Insulin Carb Ratio,IOB, Value
    """
    "System Time,Time Stamp,Carbs,Insulin Carb Ratio,IOB, Value"
    array=[["0", str(x), "0", "15", "0"] for x in range(8856)]
    if toCsv: arrayToCsv("2023", "01", "01", "dddddddd", array, t="c")
    return array
