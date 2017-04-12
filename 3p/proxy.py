import sys, socket, random
import helpers
import time
import struct

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

        s.sendto(data, destHost)
                
  finally:
      print('closing connection')
      s.sendto('&&$$__!!##@@'.encode('utf-8'), proxy_address)
     # print('{} sent packets'.format(i))
      
      s.close() #close socket