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
            decoded = data.decode('utf-8')
            print('recieved %s' %decoded)

            if data:
                tempData = decoded.upper()
                print ('sending %s back to the client' %tempData)
                connection.sendall(tempData.encode('utf-8'))
            else:
                print(client_address, ' has disconnected')
                break
    finally:
        connection.close
