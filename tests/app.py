from vgmt.oauth.server import OAUTH_Server
from vgmt.dexcom.worker import DexcomWorker
import time
from vgmt.util.csv import arrayToCsv


d = OAUTH_Server()
#d.server.requestDayData(year="2022", month="3", day="01", asList=True, )
#while len(d.unsorted_results) < 8856 :
for i in range(3):

    #d.server.requestDayData(year="2022", month="03", day=str(i+1), asList=True, asCsv=True)

    #print(len(d.server.data))
    #print(len(d.results))
    pass
# d.server.requestData(year="2022", month="01", asList=True, asCsv=True)


# print(d.workers["dexcom"].web_worker.results)
#uuid = d.requestData("dexcom", "month", "2023", "01", asCsv=True)

d.on(d.requestData, "dexcom", "month", "2023", "01", asCsv=True)

#   uuid = d.requestData("dexcom", "month", "2023", "04")
#uuid = d.requestData("dexcom", "month", "2023", "05")


while len(d.workers["dexcom"].web_worker.data) > 0:
    # print(len(d.workers["dexcom"].web_worker.unsorted_results))
    pass


d.workers["dexcom"].web_worker.join()
d.workers["dexcom"].join()
# arrayToCsv("2022", "03", "01",d.server.token,d.unsorted_results[0])
#print(d.workers["dexcom"].web_worker.unsorted_results)
#print("Average Blood Sugar " + str(int(d.workers["dexcom"].total_blood_sugar/d.workers["dexcom"].total_entries*10)/10))