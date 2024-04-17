from typing import Any
from ..util import debug
from collections import UserList
import numpy as np

class Data(UserList):

    def __init__(self, data: list):
        if (type(data) is list):
            super().__init__(data) # Pass to UserList
        else:
            super().__init__([])

    def __setitem__(self, index, item):
        self.data[index] = item

    def append(self, item):

        self.data.append(item)

    def pop(self, index=0):
        self.data.pop(index)
        print("Poping")
    def numpy(self):
        """Get array as a numpy array

        Returns:
            ndarray: Numpy Representation of the list array

        """

        return np.array(self.data,)

    def getMemorySize(self, reduce:int=8000):
        """Get amount of bytes in the array

        Arguements:
            Reduce (int): bits/unit (8000/kilobyte)
        Returns:
            int: Size of Dataset
        """
        return self.numpy().nbytes / ( reduce )
    def toOneHot(self):
        a = self.numpy()


        # Find the unique categories and their inverse indices
        categories, inverse = np.unique(a, return_inverse=True)


        # Create the one-hot encoded matrix
        one_hot = np.zeros((a.size, categories.size))

        one_hot[np.arange(a.size), inverse] = 1

        return one_hot

