#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from vgmt import __version__, STATUS, Thread, Runner
import time
import time


def test_version():
    """
    This test is marked implicitly as an integration test because the name contains "_init_"
    https://docs.pytest.org/en/6.2.x/example/markers.html#automatically-adding-markers-based-on-test-names
    """

    print(__version__)
    assert STATUS if __version__ != None else False

def test_threads():
    def execute_task(val):
    # do something threadable
        return val * 10
    r = Runner()
    t = Thread(r, self_start=False)

    @t.threaded
    def runner_fcn(values) -> list:
       results = []
       for v in range(10):
           results.append(execute_task(v))
       return results

    print(runner_fcn())

    r.setTarget(4)

    assert len(runner_fcn()) == 4



def test_runner():

    t = Thread(self_start=False)





