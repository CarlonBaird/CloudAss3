from azure.servicebus import ServiceBusService, Message, Queue
import datetime
import threading 
import time, math

bus_service = ServiceBusService(
    service_namespace='servicebusn2',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='0+T7xifpuFJ4HFCodk7D6E9bjyq0imsDE3NRzF2SMdE=')

flag = True

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
        msg = bus_service.receive_queue_message('sbqtest',peek_lock=True)
        
        if msg is not None:
            jsonData = eval(msg.body)
            data = {
    			'PartitionKey':str(jsonData['TransactionID']),
    			'RowKey':jsonData['UserId'],
    			'SellerID':jsonData['SellerID'],
    			'ProductName':jsonData['ProductName'],
    			'SalePrice':jsonData['SalePrice'],
    			'TransactionDate':jsonData['TransactionDate']
            }
            print(data)
            # table_service.insert_entity('Transactions',data)
            msg.delete()
        else:
            global flag 
            flag = False
            
if __name__=="__main__":          
    threads = {}
    while flag is True:
        for x in range(1,15):
            thread = myThread(x,'x'+str(x),x)
            threads[x] = thread
            threads[x].run()
            time.sleep(1)
    print(flag)

