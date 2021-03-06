#Brandon J. McIntyre
from azure.servicebus import ServiceBusService, Message, Queue
import datetime
import threading 
import time, math
import random
import socket
from bottle import route, run
hostname = socket.gethostname()
hostport = 2505

bus_service = ServiceBusService(
    service_namespace='servicebusn2',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='0+T7xifpuFJ4HFCodk7D6E9bjyq0imsDE3NRzF2SMdE=')

ProductName = ['Financial Trap','Failure','No Trap']

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
     			"ProductName":random.choice(ProductName),
    			"SalePrice":str(self.counter * 2),
    			"TransactionDate":str(datetime.datetime.now())
    	}
    	data = str(data)
        msg = Message(data)
        bus_service.send_queue_message('sbqtest', msg)
        
@route('/')
def printHome():
    text = "<h1>Welcome to Zanko Sender</h1>"
    text = "<a href='./sendMessages'>"+"Click to send Messages"+"</a>"
    return text

@route('/sendmessages')
def sendMessages():
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
        
if __name__=="__main__":
    run(host=hostname, port=hostport)
    
        
