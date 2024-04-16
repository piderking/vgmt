#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from vgmt import SData, __version__
from vgmt.util import Thread
from vgmt.config import  STATUS
import time
import time
import random

def test_version():
    """
    This test is marked implicitly as an integration test because the name contains "_init_"
    https://docs.pytest.org/en/6.2.x/example/markers.html#automatically-adding-markers-based-on-test-names
    """

    print(__version__)
    assert STATUS if __version__ != None else False

def test_threads():

    t = Thread(self_start=True, data=[x for x in range(1000)])

    time.sleep(5)
    t.join()

    print(t.results)
    for x in t.results:
        print("The target was {} during the datasets from percents {}% to {}%".format(len(x), x[0]/10, x[-1]/10))
    assert True


def test_numpy():
    import numpy as np

    data = SData([[120,1,0,99], [120,1,0,0], [120,1,0,0],[120,1,0,0]])

    print(data.getMemorySize(reduce=1))

