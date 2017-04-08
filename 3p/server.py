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
    #keep trying, one day you will get a file
    while(True):
      #data is a <buffer> sized chunk, addr is where it's coming from
      data, addr = s.recvfrom(buffer)

      #if the data you got is 'y'
      if(data.decode('utf-8') == 'y'):
        #open up a file named the thing below this
        f = open('receive.jpg', 'wb')

        #keep going until you got the whole thing
        while(True):
          #get more <buffer> sized chunks
          data, addr = s.recvfrom(buffer)

          #if ur done
          if(not data):
            print('you done son, come at me with another one')
            # s.close
            f.close()
            break

          #if data isn't empty print nonsense
          print(data[0])
          #stack bytes ontop of what you already have until you get a file
          f.write(data)

  finally:
      print('closing connection')
      # connection.close #close connection
        
s.close #close socket
