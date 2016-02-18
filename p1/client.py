#CS 381 Networking Project 1 - client.py
#Michael Polston
#Client for server/client relation

import socket

#create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the socket to the port where the server is listening
server_address = ('localhost', 10000) #connects to the server 'localhost' at port 10000
print('connecting to %s port %s' %server_address)
s.connect(server_address)

try:
    #send data
    message = input('input: ')
    s.sendall(message.encode('utf-8')) #sends the string encoded into utf-8

    while(message.lower() != 'exit'): #close if user enters 'exit'
        data = s.recv(200) #recieved encoded string from server
        print('recieved %s' %data.decode('utf-8')) #prints decoded string from server
        message = input('input: ')
        s.sendall(message.encode('utf-8'))
finally:
    print('closing socket')
    s.close() #closes socket
