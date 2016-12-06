#Carlon R. Baird

from azure.servicebus import ServiceBusService, Message, Queue
from azure.storage.table import TableService, Entity
import datetime
import threading 
import time, math

bus_service = ServiceBusService(
    service_namespace='servicebusn2',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='0+T7xifpuFJ4HFCodk7D6E9bjyq0imsDE3NRzF2SMdE=')

table_service = TableService(account_name='zanko', 
	account_key='THUf0H1djCIiT8G8mosZvoZGLAVgY4v4uw4TBtoUZs00k/8QxNFnbf/cEiAkUeZ5ifFLfjUFfG4FDLg3GQJT/g==')

table_service.create_table('Transactions', fail_on_exist=False)
table_service.create_table('Failures', fail_on_exist=False)

flag = True


class myThread (threading.Thread):

    def __init__(self, threadID, name, counter):
        super(myThread, self).__init__()
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
            
            #Monitoring Failures
            if data['ProductName'] is 'Failure':
                failure = {
                    'PartitionKey':data['PartitionKey'],
                    'RowKey':data['RowKey'],
                    'Time':str(datetime.datetime.now()),
                    'Status':'Failure'
                }
                
            else:
                table_service.insert_entity('Transactions',data)
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
