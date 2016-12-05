#Brandon J. McIntyre
from azure.servicebus import ServiceBusService, Message, Queue
import datetime
import threading 
import time, math

bus_service = ServiceBusService(
    service_namespace='servicebusn2',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='0+T7xifpuFJ4HFCodk7D6E9bjyq0imsDE3NRzF2SMdE=')


class myThread (threading.Thread):

    def __init__(self, threadID, name, counter):
        super(myThread, self).__init__()
        # threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
       
    
    def run(self):
        print "Starting " + self.name
        print "\n"
        data = {
     			"TransactionID":self.counter,
     			"UserId":"A"+str(self.counter),
     			"SellerID":"S",
     			"ProductName":"Financial Trap",
    			"SalePrice":str(self.counter * 2),
    			"TransactionDate":str(datetime.datetime.now())
    	}
    	data = str(data)
        msg = Message(data)
        bus_service.send_queue_message('sbqtest', msg)
    	
if __name__=="__main__":    
    i = 1
    requests = 5000000
    batch_size = int (math.floor(requests/(3600)))
    print "Batch Size :" + str(batch_size)
    for y in range(1,60): 
        threads = {}
        for x in range(1,60000):
            for z in range(1,batch_size):
                index = (i)
                thread = myThread(index,"thread-"+str(index), index)
                threads[index] = thread
                threads[index].start()
                i+=1
        #clears thread list		
        threads.clear()
        time.sleep(1)
        
