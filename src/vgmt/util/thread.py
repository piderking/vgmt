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
    def __init__(self, target: int = 3 , self_start:bool = True, daemon: bool = True, data: list or None = None) -> None:
        self.uuid: str = uuid4()
        self.total_tasks = 0 # Total Tasks Ran
        self.target = target # Target Group Amount, 3 Default
        self.tasks = 0 # Current Amount of LIVE Tasks
        self.data = [] if data is None and type(data) == list else data # Type check the data variable and make sure, list, can be empty

        threading.Thread.__init__(self, name=uuid4, daemon=daemon)
        threading.Thread

        # Self_Start
        if self_start:
            self.start()


    def run(self) -> None:
        """Not Entirely Abstract, super().run()
        """
        self.removeItem()

    def removeItem(self)-> None:
        """### Abstract Remove Method
                Currently remove from memory, other uses could be sending to cloud storage
        """
        self.data.pop(0) # Abstract Method

    def setTarget(self, val: int):
        """Set a new parallelization amount, eg: how many times the function will run depending on workload, for static threads this can remain untouched

        Args:
            val (int):
        """
        self.target = val

    def join(self) -> None:
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
            target = list(range(self.target))
            results = {}
            # We can use a with statement to ensure threads are cleaned up promptly
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(fcn, [i]): idx for idx,
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


class Runner(ABC):
    """
        ## Runner Abstract Class
        Should be used as a template in-which data processing threads can be ran off it

        ### Usage
        Initalize
    """
    data: list # Data to be processed
    def __init__(self, target: int = 3, data: list or None = None) -> None:
        self.target = target
        self.data = [] if data is None and type(data) == list else data # Type check the data variable and make sure, list, can be empty



    @abstractmethod
    def run(self,) -> None:
        """Abstraction, must be defined
        ```python
        class myRunner(Runner)"
            def __init__():
                super.__init__(target=3, data=[1,2,3])

            @t.threaded()
            def run(self):
                doSomething(self.data[0]) # Oldest Piece of Data

                return


        r = myRunner()
        t = Thread(r, self_start=False)
        ```

        """
        pass