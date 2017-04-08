#CS 381 Networking Project 1 - client.py
#Michael Polston
#Client for server/client relation
#Ran on Windows 10 in it's own terminal

import socket
import os

#create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 3000
address = socket.gethostname()
sentinel = 'exit' #string used to exit the client
buffer = 1024

#connect the socket to the port where the server is listening
server_address = (address, port) #connects to the server
print ('connecting to {}:{}'.format(server_address[0], server_address[1]))
s.connect(server_address)

choice = input('send file? (y/n): ')

try:
  if(choice == 'y'):
    s.sendto(choice.encode('utf8'), server_address)
    with open('./send.JPG', 'rb') as f:
      bytesToSend = f.read(buffer)
      s.sendto(bytesToSend, server_address)
      while(bytesToSend != ''):
        print(bytesToSend)
        if(not bytesToSend):
          break
        bytesToSend = f.read(buffer)
        s.sendto(bytesToSend, server_address)
        
finally:
    print('closing socket and exiting client')
    
s.close() #closes socket