#CS 381 Networking Project 1 - server.py
#Michael Polston
#Server for server/client relation
#Ran on Windows 10 in it's own terminal

import socket

#create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 3000
address = socket.gethostname()
decoded = ''
buffSize = 2

#bind socket to the port
server_address = (address, port)
print ('starting up on {}:{}'.format(server_address[0], server_address[1]))
s.bind(server_address) #socket is bound to the server address

#listen for connection
#s.listen(1)

while(True):
    #wait for connection
    print ('waiting for a connection')
    
    try:
        #connection, client_address = s.accept() #accept connection
        #print ('connection from: ', client_address)
        while(True):
            data, addr = s.recvfrom(buffSize) #data recieved from client
            decoded = data.decode('utf-8') #decodes client string from recieved bytes
            print('recieved: {}'.format(decoded))
            
            if data: #if data is received
                tempData = decoded.upper() #captializes decoded string
                print ('sending \'{}\' back to the client'.format(tempData)) #prints the capitalized string for refence
                tempData = tempData.encode('utf-8') #encodes tempData to send to client
                s.sendto(tempData, addr) #sends capitalized string back to client
            else:
                print(client_address, ' has disconnected')
                break
    finally:
        print('closing connection')
        connection.close #close connection
        
s.close #close socket
