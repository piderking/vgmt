from __future__ import annotations
from collections.abc import Callable, Iterable, Mapping
import concurrent.futures
from typing import Any
from ..config import MAX_THREADS, DEBUG
from ..util.debug import debug
import threading
from uuid import uuid4
import concurrent.futures
from abc import ABC, abstractmethod


tp = concurrent.futures.ThreadPoolExecutor(MAX_THREADS)

class Thread(threading.Thread):
    """# Parallelism Threading
        Utility for running opperations on or observing data in seperate paralleled threads, uses decorators with concurrent.futures

        ## Usage
        ```python
        from vgmt.util import Thread

        # Create the function, other opperations like data exporting could be done here
        # for mathmatical applications lambdas will work
        execute_task = lambda a : a * 10

        # Create an instance of the Thread object
        # For more advanced uses using subclassing and abstraction
        t = Thread(self_start=False)

        @t.threaded # Decorator from created instance
        def runner_fcn(index: int,) -> list: # index can also be _ if position isn't required
            results = []
            for v in range(10):
                results.append(execute_task(v * index)) # Lambda used to represent functionality, not required could be (v * index * 10)
            return results

        ```


    """
    def __init__(self, target: int = 3 , self_start:bool = True, daemon: bool = True, data: list or None = None) -> None:
        """Initalize Parallization Util

        Args:
            target (int, optional): Starting target of threads, auto-adjusts. Defaults to 3.
            self_start (bool, optional): If the system should autorun. Defaults to True and should stay true unless debug problems arise.
            daemon (bool, optional): If thread is dameon. Defaults to True and should stay true unless debug problems arise.
            data (list, optional): Data which is processed by threads and the adjusting system runs off of. Defaults to Empty List.
        """
        self.uuid: str = uuid4()
        self.total_tasks = 0 # Total Tasks Ran
        self.target = target # Target Group Amount, 3 Default
        self.tasks = 0 # Current Amount of LIVE Tasks
        self.data = [] if data is None and type(data) == list else data # Type check the data variable and make sure, list, can be empty
        self._work = False

        threading.Thread.__init__(self, name=uuid4, daemon=daemon)

        # Self_Start
        if self_start:
            self._work = True
            self.start()

    def run(self, index:int=0) -> None:
        """Abstract method, use to define you parallelism rules see example below, however, the following code segment must be included

        #### Required
        ```python
        super().run()
        ```
        ### Usage
        ```python

        ```
        """
        self.removeItem(index=index)

    def removeItem(self, index:int=0)-> None:
        """### Abstract Remove Method
                Currently remove from memory, other uses could be sending to cloud storage
        """
        self.data.pop(index) # Abstract Method

    def setTarget(self, val: int):
        """Set a new parallelization amount, eg: how many times the function will run depending on workload, for static threads this can remain untouched

        Args:
            val (int):
        """
        self.target = val

    def join(self) -> None:
        self._work = False

        # Kill Worker Threads
        tp.shutdown(False, cancel_futures=True)

        # Display Debug Information
        debug("Thread Information for Thread::{}:\n\tTotal Opperations Run: {}\n\tOpperations Running Curently: {}".format(self.uuid, self.total_tasks, self.tasks))

        # Finish with the thread joining
        return super().join(None)

    def __debug(self,):
        if DEBUG:
            print("Thread Information for Thread::{}:\n\tTotal Opperations Run: {}\n\tOpperations Running Curently: {}".format(self.uuid, self.total_tasks, self.tasks))

    def threaded(self: Thread, fcn):
        """ ## Threading Decorator
            Runs a paralized task for the amount in the target

        """
        def wrapper(*args, **kwargs):
            target = list(range(self.target)) # Length
            results = {}
            # We can use a with statement to ensure threads are cleaned up promptly
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(fcn, i): idx for idx,
                            i in enumerate(target)} # { Future: Submit}

                # Amount of Tasks
                tasks = len(futures)

                # Add to total running
                self.tasks += tasks
                self.total_tasks += tasks
                # Rounding
                tenth = round(tasks / 10)
                debug('Formed pool of {} tasks'.format(tasks))

                for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                    i = futures[future] # Future
                    try:
                        # store result
                        data = future.result()

                        # check to see if in array form
                        if len(data) == 1:
                            data = data[0]
                        results[i] = data

                        self.tasks -= 1
                    except Exception as exc:
                        self.tasks -= 1
                        debug('{} generated an exception: {}'.format(
                            target[i], exc))

                    if DEBUG and tenth != 0 and idx != 0 and idx % tenth == 0:
                        debug('{}% Done'.format((idx // tenth) * 10))

            # sort and put in array
            final = []
            for k, v in sorted(results.items()):
                final.append(v)

            return final
        return wrapper
