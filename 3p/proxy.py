import sys, socket, random
import helpers
import time
import struct
import random

sendPort = helpers.ports['send']
proxPort = helpers.ports['proxy']
destPort= helpers.ports['dest']

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
# dropRate = 90
#s.sendto(choice.encode('utf8'), destHost)
while True:
#wait for connection
  try:
    #keep trying, one day you will get a connection
    while(True):
      #get more <buffer> sized chunks
      data, addr = s.recvfrom(buffer)
      if(random.random()*100 > float(dropRate)):
        # print('address[1]: ', addr[1], '\nsend[1]: ', sendHost[1], '\ndest: ', destHost[1])
        if(addr[1] == sendHost_address[1]):
          #send to sender
          # print('sender')
          s.sendto(data, destHost)
        elif(addr[1] == destHost_address[1]):
          #send to dest
          print('dest')
          s.sendto(data, sendHost)
      else:
        print('Dropped packed from', addr)
  finally:
      print('closing connection')
      s.sendto('&&$$__!!##@@'.encode('utf-8'), proxy_address)
     # print('{} sent packets'.format(i))
      
      s.close() #close socket