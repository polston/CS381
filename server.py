import socket
#create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind socket to the port
server_address = ('localhost', 10000)
print ('starting up on %s port %s' %server_address)
s.bind(server_address)

#listen for connection
s.listen(1)

while(True):
    #wait for connection
    print ('waiting for a connection')
    connection, client_address = s.accept()

    try:
        print ('connection from: ', client_address)
        while(True):
            data = connection.recv(100)
            print('recieved %s' %data.decode('utf-8'))
            if data:
                print ('sending data back to the client')
                tempData = data.decode('utf-8')
                connection.sendall(tempData.encode('utf-8'))
            else:
                print('no more data from: ', client_address)
                break
    finally:
        connection.close
