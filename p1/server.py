#CS 381 Networking Project 1 - server.py
#Michael Polston
#Server for server/client relation
#Ran on Ubuntu 15 in separate terminals

import socket

#create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind socket to the port
server_address = ('localhost', 10000) #server address is 'localhost' with port 10000 open
print ('starting up on %s port %s' %server_address)
s.bind(server_address) #socket is bound to the server address

#listen for connection
s.listen(1)

while(True):
    #wait for connection
    print ('waiting for a connection')
    connection, client_address = s.accept() #accept connection

    try:
        print ('connection from: ', client_address)
        while(True):
            data = connection.recv(200)
            decoded = data.decode('utf-8') #decodes client string
            print('recieved %s' %decoded)

            if data: #if data is received
                tempData = decoded.upper() #captializes decoded string
                print ('sending %s back to the client' %tempData) #prints the capitalized string for refence
                connection.sendall(tempData.encode('utf-8')) #sends capitalized string back to client
            else:
                print(client_address, ' has disconnected')
                break
    finally:
        connection.close #close socket if closed
