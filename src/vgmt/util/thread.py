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
import math

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
        t = Thread(self_start=True)

        @t.threaded # Decorator from created instance
        def runner_fcn(index: int,) -> list: # index can also be _ if position isn't required
            results = []
            for v in range(10):
                results.append(execute_task(v * index)) # Lambda used to represent functionality, not required could be (v * index * 10)
            return results

        ```


    """
    def __init__(self, target: int = 3 , self_start:bool = True, daemon: bool = True, data: list = [], basis: float = 0.75, times: int = 3) -> None:
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
        self.data = [] if data is None or type(data) is not list else data # Type check the data variable and make sure, list, can be empty
        self.results = []
        self._work = False
        self.basis = basis
        self.times = times
        self.sameTarget = 0
        threading.Thread.__init__(self, name=uuid4, daemon=daemon)

        # Self_Start
        if self_start:
            self._work = True
            self.start()


    def setFcn(self, fcn):
        self.fcn = fcn # Function

    def fcn(self, i, d):
        print("Index: {} Data, {}".format(str(i), str(d)))

        return [d]

    def run_fcn(self,):
        """If the data needs operations, for when their is data inside the
        """
        if callable(self.fcn):
            self.threaded(self.fcn)()
            self.removeItem()

        else:
            # This will occur when function is not initalized (yet)
            if self.fcn is None:
                debug("Function not set yet -- Thread.setFcn(fcn)")
            else:
                debug("Function called for {} could not be executed: Not callable".format(str(type(self.fcn))))

    def needsOpperation(self):
        return True if len(self.data)/3 > 0 else False #

    def run(self,) -> None:
        """Abstract method, use to define you parallelism rules see example below, however, the following code segment must be included

        #### Required
        ```python
        super().run()
        ```
        ### Usage
        ```python

        ```
        """
        while self._work:
            if self.needsOpperation():
                if len(self.data) >= self.target:
                    self.sameTarget += 1

                    if self.sameTarget == self.times and math.ceil(self.target * (1+self.basis)) < len(self.data):
                        self.setTarget(math.ceil(self.target * (1+self.basis))) # Increate the target if the value is greater than basis increate of the target and the target has been reached 3 times

                    self.run_fcn()
                else:
                    self.setTarget(len(self.data))
                    self.run_fcn()


    def removeItem(self)-> None:
        """### Abstract Remove Method
                Currently remove from memory, other uses could be sending to cloud storage
        """
        if self.needsOpperation() and type(self.data) is list:
            # debug(self.data[0]) # See outcoming data
            # TODO Optimize Algorithm prediction thread
            for i in range(self.target):
                if len(self.data) > 0:
                    self.data.pop(0) # Abstract Method
                else:
                    raise IndexError("The data list does not contain the index 0, if this error went wrong file bug report: \n\t Data::{}".format(str(self.data)))


    def setTarget(self, val: int):
        """Set a new parallelization amount, eg: how many times the function will run depending on workload, for static threads this can remain untouched

        Args:
            val (int):
        """
        self.sameTarget = 0
        self.target = val

    def join(self) -> None:
        self._work = False

        # Kill Worker Threads
        tp.shutdown(False, cancel_futures=True)

        # Display Debug Information
        debug("Thread Information for Thread::{}:\n\tTotal Opperations Run: {}\n\tOpperations Running Curently: {}\n\tTarget Amount: {}".format(self.uuid, self.total_tasks, self.tasks, self.target))

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
            target = list(range(self.target)) # range(self.target if len(self.data)/self.target >= 1 else len(self.data))
            results = {}
            # We can use a with statement to ensure threads are cleaned up promptly
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(fcn, i, self.data[i]): idx for idx,
                            i in enumerate(target)} # { Future: Submit}

                # Amount of Tasks
                tasks = len(futures)

                # Add to total running
                self.tasks += tasks
                self.total_tasks += tasks
                # Rounding
                tenth = round(tasks / 10)
                # debug('Formed pool of {} tasks'.format(tasks))

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


            # sort and put in array
            final = []
            for k, v in sorted(results.items()):
                final.append(v)
            self.results.append(final)
            return final
        return wrapper
