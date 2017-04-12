import sys, socket, random
import helpers
import time

sendPort = 3000
proxPort = 3001
destPort=3002

address = socket.gethostname()
buffer = helpers.buffer
decoded = ''
received = 'ACK'
choice = 'y'
i=0

#create a UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
proxy_address = (address, proxPort)
sendHost_address = (address, sendPort)
destHost_address = (address, destPort)

print ('starting up on {}:{}'.format(proxy_address[0], proxy_address[1]))
s.bind(proxy_address)

sendHost = sendHost_address
destHost = destHost_address

dropRate = input('Whats the drop rate of this proxy? (0-100)%\n')
#s.sendto(choice.encode('utf8'), destHost)
while True:
#wait for connection
  try:
    #keep trying, one day you will get a connection
    while(True):
        #get more <buffer> sized chunks
        data, addr = s.recvfrom(buffer)
        # print('data: ', data, ' addr: ', addr)
        
        if(data):
            #if ur done
            if(data.decode('utf-8') == '&&$$__!!##@@'):
                #time.sleep(0.001)
                print('No more packets to forward - exiting program')
                s.sendto(data, destHost)
                sys.exit() #close the program
                break
            else:
                # print('Recieved Packet: {}'.format(data))
                # s.sendto(received.encode('utf8'), sendHost) #I don't know what this line is doing - "supposed" to be ACK
                #print('ACK Sent')
                #if(random.uniform(0,100) <= int(dropRate)):
                 # i+=1  
                #s.sendto(data, sendHost)
                s.sendto(data, destHost)
                #time.sleep(0.01)
                #time.sleep(0.001)
                i+=1
                #print('{} packets sent'.format(i))
                # print('Sent Packet: {}'.format(data))

                
  finally:
      print('closing connection')
      s.sendto('&&$$__!!##@@'.encode('utf-8'), proxy_address)
     # print('{} sent packets'.format(i))
      
      s.close() #close socket