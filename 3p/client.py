#CS 381 Networking Project 1 - client.py
#Michael Polston
#Client for server/client relation
#Ran on Windows 10 in it's own terminal

import socket

#create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 3000
address = socket.gethostname()
sentinel = 'exit' #string used to exit the client
buffer = 2048

#connect the socket to the port where the server is listening
server_address = (address, port) #connects to the server
print ('connecting to {}:{}'.format(server_address[0], server_address[1]))
s.connect(server_address)

message = input('input: ')

try:
    if(message != sentinel):
        #send data initially
        message = message.encode('utf-8') #encodes message into readable text
        s.sendto(message, server_address) #sends the encoded string
    
        #send data inside connection
        while(True):
            data = s.recvfrom(buffer) #recieved encoded string from server
            print(str(data))
            data = data[0].decode('utf-8')
            print('recieved: {}'.format(data)) #prints decoded string from bytes
            message = input('input: ')
            if(message == sentinel):
                break
            message = message.encode('utf-8')
            s.sendto(message, server_address)
        
finally:
    print('closing socket and exiting client')
    
s.close() #closes socket