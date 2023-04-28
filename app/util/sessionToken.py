from uuid import uuid4
class SessionToken(object):
    _sessionToken: str
    canIdentifyDebug: bool

    @property
    def sessionToken(self,) -> str:
        """Session Token Getter

        Returns:
            str: Session Token as a String
        """
        return self._sessionToken
    # @sessionToken.setter
    def sessionToken(self, newSessionToken:str, oldSessionToken: str) -> bool | ValueError:
        if oldSessionToken == self.sessionToken and oldSessionToken[:5] == "vgmt:":
            print("New Session Started!")
            self._sessionToken = newSessionToken
            return True
        else:
            # Give some useful Debug Info
            raise ValueError("Session Token failed to identify, throwing program error.\nOld Session Token: {}, Given Session Token: {}, Replacement Session Token: {}".format(
                self.sessionToken if self.canIdentifyDebug else "Hidden By Operator", oldSessionToken, newSessionToken
            ))
        
    @classmethod
    def generateRandomSession(_cls):
        """Generate a VGMT Session

        Returns:
            str: VGMT Session, format: vgmt:3dedc52e-5821-493d-bd13-5019c86f6d41
                vgmt:uuid4
        """
        return "vgmt:{}".format(str(uuid4()))
    
    def validate(self, session: str) -> bool:
        """Validates on String Pairs on session object itself

        Args:
            session (str): Session as a string; sessionObject.sessionToken

        Returns:
            bool: Wether it worked or note
        """
        # Will be called for validating other sessions VALID_SESSION is the session() here
        return True if self.sessionToken == session() and self.sessionToken[:5] == "vgmt:" else False
    def __call__(self,) -> str:
        """Get Session Token

        Returns:
            str: Session Token
        """
        return self.sessionToken # Get the Session Token more elinquentaly
    def __init__(self, sessionToken: str | None = None, canIdentifyDebug: bool = False) -> None:
        """Session Token Object

        Args:
            canIdentifyDebug (bool, optional): _description_. Defaults to False.
        """
        self.sessionToken = self.generateRandomSession() if sessionToken is None else sessionToken
        self.canIdentifyDebug = canIdentifyDebug

# Going to be defined in __main__.py
VALID_SESSION_TOKEN: SessionToken | None = SessionToken(canIdentifyDebug=True)
# print(VALID_SESSION_TOKEN.validate(VALID_SESSION_TOKEN)) 

def validateWrapper(sessionToken: SessionToken | None = None):
    """Validate a Session Token

    Args:
        sessionToken (SessionToken): Session Token Object
    """
    if VALID_SESSION_TOKEN is None:
                raise ValueError("Base Token isn't initalized prior to being read")
    def decorator(func):
        def wrapper(*args, **kwargs) :
            "This is the wrapper function"
            if sessionToken is None:
                if kwargs["sessionToken"] is type(SessionToken):
                    if kwargs["sessionToken"].validate(VALID_SESSION_TOKEN):
                        # If Session Token if hidden in kwargs
                        kwargs["accept"] = True
                        return func(args, kwargs)
                    else:
                        raise ValueError("No Input Given")
                else:
                    raise ValueError("Input Token is None")
            
            if sessionToken.validate(VALID_SESSION_TOKEN): # Compare Given (object) to CURRENT (stored in variable)
                kwargs["accept"] = True
                return func(args, kwargs)
            else:
                raise ValueError("Base Token isn't initalized prior to being read")
        return wrapper
    return decorator


@validateWrapper(sessionToken=None)
def validate(sessionToken: SessionToken | None = None, accept:bool=False) -> bool:
    """Validate a Session Token
    
    Args:
        sessionToken (SessionToken): Session Token Object

    Returns:
        bool: If the session is valid; alway yes because if the process fails the whole system collapses
    """
    # Return the kwargs accept, which is set by the decorator if the session token provided
    return accept