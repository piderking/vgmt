from ..data import Data

class DexcomData(Data):
    def __init__(self):
        self.key = ("Blood Sugar")
        super().__init__([], self.key)