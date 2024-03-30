from ..config import DEBUG

def debug(obj: object):
    """Writes to STDOUT if debug config is true

    Args:
        obj (object): Object to be written to STDOUT
    """
    try:
        obj.__debug()
    except Exception as e:
        if DEBUG: print(obj)