#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from vgmt import __version__, STATUS
from vgmt.util import Thread
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
    execute_task = lambda a : a * 10

    t = Thread(self_start=False)

    @t.threaded
    def runner_fcn(index: int,) -> list:
        """_summary_

        Args:
            index (int): Index in which the function is in parralization

        Returns:
            list: _description_
        """
        print(index)
        results = []
        for v in range(10):
            results.append(execute_task(v * index))
        return results

    num = 4
    t.setTarget(num)
    print()
    assert len(runner_fcn()) == 4

