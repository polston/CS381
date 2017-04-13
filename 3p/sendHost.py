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

# choice = input('send file? (y/n):\n')
choice = 'y'
chunked = []
unChunked = []


try:
  if(choice == 'y'):
    i = 0 #chunk index
    
    # filename = input('File path? (\'./filename.extension\' for current directory)')
    filename = './send.jpg'
    chunkSize = helpers.getFileSize(filename)
    tChunks = helpers.getNumChunks(filename)
    

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
        chunked.append(helpers.wrapChunk(helpers.codes['sending'], i, tChunks, bytesToSend))
        
        #this doesn't really need to go here, but it verifies that packed and unpacked structs are the same
        #i.e. that the bytes are correct
        unChunked.append(helpers.unwrapChunk(chunked[i]))
        
        
        #increments for the index of the chunk
        i += 1

  i = 0
  for chunk in chunked:
    s.sendto(chunk, proxy_address)
    # print(helpers.rawUnwrap(chunk))
    # time.sleep(0.0001)
    # print(i) # current chunk being sent
    i += 1
  while(True):
    s.sendto(helpers.codeWrap(helpers.codes['done']), proxy_address)

#ur done
finally:
  #prints to look at individual wrapped/unwrapped chunks
  print('chunked: ', sys.getsizeof(chunked[1]))
  print('------------------')
  print('unchunked: ', sys.getsizeof(unChunked[1]))

  #prints the arrays of matching and unmatching indexes
  # print(helpers.compareChunks(chunked, unChunked))

  s.close() #closes socket