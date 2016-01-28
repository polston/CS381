import socket

#create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' %server_address)
s.connect(server_address)

try:
    #send data
    message = input('input: ')
    s.sendall(message.encode('utf-8'))

    while(message.lower() != 'exit'):
        data = s.recv(100)
        print('recieved %s' %data.decode('utf-8'))
        message = input('input: ')
        s.sendall(message.encode('utf-8'))
finally:
    print('closing socket')
    s.close()
