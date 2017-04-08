#Michael Polston
#CS381 Project 2
#Single program acting as both client and server in two-way chatroom.

import socket
import sys

port = 3000
buff_size = 2048
sentinel = 'exit' #string used to exit/close the client/server

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


choice = input('Choose from the following:\n1. Host server\n2. Join server\nInput option 1 or 2: ')

#chose to host server
if(choice is '1'):
    print('Hosting server')
    
    #attempts to open server 
    try:
        server_sock.bind(('localhost', port))
    except socket.error as e:
        print(str(e))
    
    #listens for connections
    server_sock.listen(5)
    
    while(True):
        try:
            #accepts incoming connection
            connection, client_address = server_sock.accept()
            print ('connection from: ' + client_address[0] + ':' + str(client_address[1]))
            #while connected to client
            while(connection):
                
                #decode incoming message
                data = connection.recv(buff_size)
                data = data.decode('utf-8')
                
                if(data):
                    #print data out and prompt server-side client to send a message
                    print('destination: ' + data)
                    #check if the server-side client has entered 'exit'
                    if(data == sentinel):
                        break
                    data = input('source: ')
                    connection.sendall(data.encode('utf-8'))
                        
                #if the client disconnects
                else:
                    print(client_address[0] + ':' + str(client_address[1]) + ' disconnected')
                    client_sock.close()
                    break
                    
        #break on a socket error, essentially just if the client closes the connection first
        except socket.error as e:
            server_sock.close()
            break
        
        #probably somewhat redundant 'finally' statement
        finally:
            server_sock.close()
            print('Received \'exit\' server shuting down')
            break
            

#option chosen to join server
elif(choice is '2'):
    print('Joining server')
    
    #for testing
    #server_address = ('localhost', 3000)
    
    server_IP = input('Input server IP: ')
    server_address = (server_IP, port)
    
    #attempt to connect to server
    try:
        #connect to server
        client_sock.connect(server_address)
        print('Connected to: ' + server_address[0] + ':' + str(port))
        
        #initial message to server
        message = input('source: ')
        client_sock.sendall(message.encode('utf-8'))
        
        #if the message isn't 'exit'
        if(message != sentinel):
            while(True):
                #receive data and decode it from the server
                data = client_sock.recv(buff_size)
                data = data.decode('utf-8')
                
                #if the decoded data string received isn't 'exit'
                if(data):
                    #print out the data
                    print('destination: ' + data)
                    
                    #if data received is 'exit'
                    if(data == sentinel):
                        print('Received \'exit\' disconnected from: ' + server_address[0] + ':' + str(port))
                        break
                    
                    #prompt client to send message
                    message = input('source: ')
                    client_sock.sendall(message.encode('utf-8'))
                    
                    #if the message being sent is 'exit', disconnect
                    if(message == sentinel):
                        print('Sent \'exit\' disconnected from: ' + server_address[0] + ':' + str(port))
                        break
                else:
                    client_sock.close()
                    print('Disconnected from: ' + server_address[0] + ':' + str(port))
                    break
        else:
            client_sock.close()
            print('Disconnected from: ' + server_address[0] + ':' + str(port))
    except socket.error as e:
        client_sock.close()
        print('Unable to connect to: ' + server_address[0] + ':' + str(port) + '\nReceived error: ' + str(e))
        