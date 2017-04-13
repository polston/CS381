#CS 381 Networking Project 3 - rcvHost.py
#Michael Polston, Austin Little
#Receiving host for proxy
#

import socket
import sys
import helpers
import time
import io
import struct
import math

#create UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

proxPort = 3001
destPort = 3002
address = socket.gethostname()
decoded = ''
buffer = helpers.buffer
chunkBytes = helpers.chunkBytes

#bind socket to the port
destHost_address = (address, destPort)
print ('starting up on {}:{}'.format(destHost_address[0], destHost_address[1]))
s.bind(destHost_address) #socket is bound to the server address

tempFile = []

i = 0
j = 0

while(True):
  try:    
    while(True):
      timer1 = time.time()
      data, addr = s.recvfrom(buffer)
      # print(helpers.codeUnwrap(data)[0] == helpers.codes['done'])
      # if(helpers.rawUnwrap(data)[0] == b'done'):
      # print()
      if(helpers.codeUnwrap(data)[0] == helpers.codes['done']):
        print('received done')
        sys.exit()
        break
      
      else:
        chunk = helpers.unwrapChunk(data)
        tempFile.append(chunk)

      
      timer2 = time.time()
      # print(timer2-timer1)

      #TODO: do better than a crappy timer to figure out when to disconnect
      #you have 10 seconds to start sending the file
      if(timer2 - timer1 == 10):
        sys.exit()
        break


  finally:
    print('closing connection')
    missing = helpers.missingIndexes(tempFile)
    missingChunks = []
      
    missingChunks = helpers.wrapMissing(missing)
    print(missingChunks)
    
    # helpers.verifyNumberOfChunks(tempFile, tempFile[0][1])
    # print(helpers.compareIndexes(tempFile))

    helpers.writeFile(tempFile, 'output', '.jpg')
    print('done')