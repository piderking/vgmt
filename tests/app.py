from vgmt.dexcom.server import DexcomOAuthServer
from vgmt.dexcom.worker import DexcomWorker

#d = DexcomOAuthServer()
d = DexcomWorker(self_start=True)

d.server.requestData("2022", "03", asList=True)
while len(d.unsorted_results) < 8856 :
    print(len(d.unsorted_results))
    #print(len(d.server.data))
    #print(len(d.results))
    pass

d.join()