

from typing import Any
from ..util import debug
from collections import UserList
import numpy as np
class Data(UserList):

    def __init__(self, data, key: str or list = "DEFAULT"):
        self.key: str or list = key if not key == "DEFAULT" else ( # Default Data Point Key
                "Time_Stamp", "Blood_Sugar", "Heat_Rate", "Insulin_On_Board"
        )
        super().__init__(data)

    def __setitem__(self, index, item):
        self.data[index] = item

    def append(self, item):

        self.data.append(item)

    def numpy(self):
        """Get array as a numpy array

        Returns:
            ndarray: Numpy Representation of the list array
        """
        return np.array(self.data)

    def toOneHot(self):
        a = self.numpy()


        # Find the unique categories and their inverse indices
        categories, inverse = np.unique(a, return_inverse=True)


        # Create the one-hot encoded matrix
        one_hot = np.zeros((a.size, categories.size))

        one_hot[np.arange(a.size), inverse] = 1

        return one_hot

    def toTable(self):
        dts = {'names': tuple(self.key),'formats':(np.int16, np.int16, np.int16, np.int16)}

        array = np.array(self.data, dtype=dts)

        return array
