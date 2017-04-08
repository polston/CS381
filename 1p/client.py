#CS 381 Networking Project 1 - client.py
#Michael Polston
#Client for server/client relation
#Ran on Windows 10 in it's own terminal

import socket

#create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 3000
address = 'localhost'
sentinel = 'exit' #string used to exit the client

#connect the socket to the port where the server is listening
server_address = (address, port) #connects to the server
print ('connecting to {}:{}'.format(server_address[0], server_address[1]))
s.connect(server_address)

message = input('input: ')

try:
    if(message != sentinel):
        #send data initially
        message = message.encode('utf-8') #encodes message into readable text
        s.sendall(message) #sends the encoded string
    
        #send data inside connection
        while(True):
            data = s.recv(200) #recieved encoded string from server
            data = data.decode('utf-8')
            print('recieved: {}'.format(data)) #prints decoded string from bytes
            message = input('input: ')
            if(message == sentinel):
                break
            message = message.encode('utf-8')
            s.sendall(message)
        
finally:
    print('closing socket and exiting client')
    
s.close() #closes socket