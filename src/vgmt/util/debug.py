from ..config import DEBUG, MAX_DEBUGS
from colorama import Fore, Back, Style
colors = {
    "error":Fore.RED,
    "critical":Fore.BLACK+Back.RED,
    "ok":Fore.YELLOW,
    "warn":Fore.LIGHTRED_EX,
    "sucess":Fore.GREEN,
    "general":Fore.BLACK,
    "info":Fore.BLUE,
    "important":Back.CYAN,

}
last_messages = ["" for _ in range(10)]
def debug(obj: object, type: str="general"):
    """Writes to STDOUT if debug config is true

    Args:
        obj (object): Object to be written to STDOUT
    """
    times = 0
    for message in last_messages:
        if str(obj) == message:
            times += 1

    if times >= MAX_DEBUGS: # if we don't have to mess around with data then lets not
        return
    last_messages.pop(0)
    last_messages.append(str(obj))
    try:
        obj.__debug()
    except Exception as e:
        if DEBUG: print(colors[type.strip().lower()]+obj+Style.RESET_ALL)