from __future__ import annotations
from collections.abc import Callable, Iterable, Mapping
import concurrent.futures
from typing import Any
from ..config import MAX_THREADS, DEBUG
from ..util.debug import debug
import threading
from uuid import uuid4
import concurrent.futures


tp = concurrent.futures.ThreadPoolExecutor(MAX_THREADS)

class Thread(threading.Thread):
    def __init__(self, runner: Runner, self_start:bool = True, daemon: bool = True) -> None:
        self.uuid: str = uuid4()
        self.total_tasks = 0 # Total Tasks Ran
        self.target = 3 # Target Group Amount, 3 Default
        self.tasks = 0 # Current Amount of LIVE Tasks
        self.runner = None
        threading.Thread.__init__(self, name=uuid4, daemon=daemon)
        threading.Thread

        # Self_Start
        if self_start:
            self.start()

    def run(self) -> None:
        # This is where decorator should be run
        pass

    def join(self) -> None:
        # Kill Worker Threads
        tp.shutdown(False, cancel_futures=True)
        # Finish with the thread joining
        return super().join(None)

    def threaded(self: Thread, fcn):
        def wrapper(*args, **kwargs):
            results = {}
            # We can use a with statement to ensure threads are cleaned up promptly
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(fcn, [i]): idx for idx,
                            i in enumerate(args[0])} # Run the tasks

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
                            args[0][i], exc))

                    if DEBUG and tenth != 0 and idx != 0 and idx % tenth == 0:
                        debug('{}% Done'.format((idx // tenth) * 10))

            # sort and put in array
            final = []
            for k, v in sorted(results.items()):
                final.append(v)

            return final
        return wrapper


class Runner:
    """# Task Runner Class
        Run tools like processing data here
        ## Structure

        ```python
        # Create Thread Instance
        thread = Thread()

        # Call with decorator
        @thread.threaded
        def run
        ```
    """
    def __init__(self) -> None:
        pass