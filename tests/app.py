from vgmt.dexcom.server import DexcomOAuthServer
from vgmt.dexcom.worker import DexcomWorker
import time
#d = DexcomOAuthServer()
d = DexcomWorker(self_start=True)

d.server.requestDayData(year="2022", month="3", day="01", asList=True)
#while len(d.unsorted_results) < 8856 :
for i in range(5):
    d.server.requestDayData(year="2022", month="03", day=str(i+1), asList=True)

    print(len(d.unsorted_results))

    #print(len(d.server.data))
    #print(len(d.results))
    pass

d.join()
print("Unsorted Length Results " + str(len(d.unsorted_results)))
