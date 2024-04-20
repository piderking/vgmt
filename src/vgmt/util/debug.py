from ..config import DEBUG
from colorama import Fore, Back, Style
colors = {
    "error":Fore.RED,
    "critical":Fore.BLACK+Back.RED,
    "ok":Fore.YELLOW,
    "sucess":Fore.GREEN,
    "general":Fore.BLACK,
    "info":Fore.BLUE,
    "important":Back.CYAN,

}
def debug(obj: object, type: str="general"):
    """Writes to STDOUT if debug config is true

    Args:
        obj (object): Object to be written to STDOUT
    """

    try:
        obj.__debug()
    except Exception as e:
        if DEBUG: print(colors[type.strip().lower()]+obj+Style.RESET_ALL)