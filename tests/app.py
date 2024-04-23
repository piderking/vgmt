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


while len(d.data) > 0: # Wating til end of program
    pass
d.join()
# arrayToCsv("2022", "03", "01",d.server.token,d.unsorted_results[0])
print("Unsorted Length Results " + str(len(d.unsorted_results)))
print("Average Blood Sugar " + str(int(d.total_blood_sugar/d.total_entries*10)/10))