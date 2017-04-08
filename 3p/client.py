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

    #send 'y' to the server, to let it know it's going to get the file
    s.sendto(choice.encode('utf8'), server_address)

    #open up the file you're going to send
    with open('./send.JPG', 'rb') as f:
      #read <buffer> amount of the file
      bytesToSend = f.read(buffer)
      #send <buffer> amount of the file to the server
      s.sendto(bytesToSend, server_address)
      #while there are bytes to send
      while(bytesToSend != ''):
        #print gobbledygook
        print(bytesToSend)
        #if you're done, leave
        if(not bytesToSend):
          break
        #if you have more bytes to send, get 'em
        bytesToSend = f.read(buffer)
        #get those bytes OUTTA HERE
        s.sendto(bytesToSend, server_address)

#ur done
finally:
    print('closing socket and exiting client')
    
s.close() #closes socket