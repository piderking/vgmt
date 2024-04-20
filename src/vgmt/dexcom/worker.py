from ..util import Thread
from .server import DexcomOAuthServer
import math
class DexcomWorker(Thread):

    def __init__(self, self_start: bool = True) -> None:
        self.self_start = self_start
        self.server = DexcomOAuthServer(self_start=self_start) # Initalize the Server
        super().__init__(self_start=self_start)

    def start(self) -> None:
        if not self.self_start: self.server.start() # Start the Server
        return super().start()

    def fcn(self,index: int, data:list):
        #for d in data:
        #    print(d)
        return [data]

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
            for new_data in self.server.data: # Take new data and transfer it from the server
                    # print("Adding Additional Data")
                    self.data.append(new_data)
                    self.server.data.pop(0)
            if self.needsOpperation():
                if len(self.data) >= self.target:
                    self.sameTarget += 1

                    # TODO Optimize Algorithm prediction thread
                    if self.sameTarget == self.times and math.ceil(self.target * (1+self.basis)) < len(self.data):
                        self.setTarget(math.ceil(self.target * (1+self.basis))) # Increate the target if the value is greater than basis increate of the target and the target has been reached 3 times

                    self.run_fcn()
                else:
                    self.setTarget(len(self.data))
                    self.run_fcn()