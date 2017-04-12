#CS 381 Networking Project 3 - client.py
#Michael Polston, Austin Little
#Client for server/client relation
#Ran on Windows 10 in it's own terminal

import socket
import os
import os.path
import time
import helpers
import sys
import io

#create a UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sendPort = 3000
proxPort = 3001
address = socket.gethostname()
buffer = helpers.buffer
chunkBytes = helpers.chunkBytes
decoded = ''
sendHost_address = (address, sendPort)
i = 0
j = 0

#connect the socket to the port where the server is listening
proxy_address = (address, proxPort) #connects to the server
print ('starting up on {}:{}'.format(sendHost_address[0], sendHost_address[1]))
print ('connecting to {}:{}'.format(proxy_address[0], proxy_address[1]))
s.bind(sendHost_address)
#s.connect(proxy_address)

choice = input('send file? (y/n):\n')

chunked = []
unChunked = []


try:
  if(choice == 'y'):
    i = 0 #chunk index
    
    #send 'y' to the server, to let it know it's going to get the file
    #s.sendto(choice.encode('utf8'), server_address)
    
    #open up the file you're going to send
    file = './send.jpg'
    chunkSize = helpers.getFileSize(file)
    tChunks = helpers.getNumChunks(file)

    print('file size: ', chunkSize)
    print('# of chunks: ', tChunks)

    #opens the sending file to read from it
    with open('./send.jpg', 'rb') as f:
      while(True):
        bytesToSend = f.read(chunkBytes)

        #if you're done, leave / close the file
        if(not bytesToSend):
          f.close()
          break
        
        #makes an array of chunks in structs / converted to bytes
        chunked.append(helpers.wrapChunk(i, tChunks, bytesToSend))
        #this doesn't really need to go here, but it verifies that packed and unpacked structs are the same
        #i.e. that the bytes are correct
        unChunked.append(helpers.unwrapChunk(chunked[i]))
        
        #increments for the index of the chunk
        i += 1

  #removes file if it already exists
  if(os.path.isfile('./receive.jpg')):
    print('removing receive.jpg')
    os.remove('./receive.jpg')
  
  #initializes a bytes variable
  byteFile = b''

  #concatenates all of the unchunked things into a single bytes type
  for chunk in unChunked:
    byteFile += chunk
  
  # print("Native byteorder: ", sys.byteorder)

  #writes the byteFile to a file
  with io.open('./receive.jpg', 'wb') as f:
    f.write(byteFile)
  f.close()

#ur done
finally:

  #prints to look at individual wrapped/unwrapped chunks
  print('chunked: ', chunked[1])
  print('------------------')
  print('unchunked: ', unChunked[1])

  #prints the arrays of matching and unmatching indexes
  # print(helpers.compareIndexes(chunked, unChunked))

  s.close() #closes socket