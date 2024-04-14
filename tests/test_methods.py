#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from vgmt import __version__, STATUS, Data
from vgmt.util import Thread
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
    execute_task = lambda a : a * 10

    t = Thread(self_start=True, data=[x for x in range(10)])

    @t.threaded
    def runner_fcn(index: int,data) -> list:
        """_summary_

        Args:
            index (int): Index in which the function is in parralization
            data (data in the parralization)

        Returns:
            list: _description_
        """
        results = []
        print("Data is " + str(data))
        for v in range(10):
            results.append(execute_task(v * index * data))
        print(str(index) + " :: " +  str(results))
        return results

    t.setFcn(runner_fcn)
    # print(len(runner_fcn()) == 4)

    # time.sleep(5)
    t.join()
    assert True


def test_numpy():
    import numpy as np

    data = Data([[120,1,0,99], [120,1,0,0], [120,1,0,0],[120,1,0,0]])



    print(data.toTable())

