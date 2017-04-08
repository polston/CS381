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
buffer = 1024

#bind socket to the port
server_address = (address, port)
print ('starting up on {}:{}'.format(server_address[0], server_address[1]))
s.bind(server_address) #socket is bound to the server address

#listen for connection
#s.listen(1)

while(True):
    #wait for connection
  try:
    while(True):
      #data, addr = s.recvfrom(buffer)
      data, addr = s.recvfrom(buffer)
      if(data.decode('utf-8') == 'y'):
        f = open('receive.jpg', 'wb')
        while(True):
          data, addr = s.recvfrom(buffer)
          if(not data):
            print('you done son, come at me with another one')
            # s.close
            break
          print(data[0])
          f.write(data)

  finally:
      print('closing connection')
      # connection.close #close connection
        
s.close #close socket
