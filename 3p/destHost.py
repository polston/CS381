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
      print()
      if(helpers.codeUnwrap(data)[0] == helpers.codes['done']):
        print('received done')
        sys.exit()
        break
      
      else:
        chunk = helpers.unwrapChunk(data)
        tempFile.append(chunk)

      
      timer2 = time.time()
      print(timer2-timer1)

      #TODO: do better than a crappy timer to figure out when to disconnect
      #you have 10 seconds to start sending the file
      if(timer2 - timer1 == 10):
        sys.exit()
        break


  finally:
    print('closing connection')
    # print('')
    missing = helpers.missingIndexes(tempFile)
    # print('missing: ', missing)
    # packedMissing = b'missing' + struct.pack('{}i'.format(len(missing)), *missing)
    # print('packedmissing: ', packedMissing)
    # print('pmissing len: ', len(packedMissing))
    for i in missing:
      print(i)
    # # for index in missing:
    # #   packedMissing = struct.pack('i', index)# byte reprsentation of the integers
    # #   print(packedMissing) 
    # # print('packedMissing: ', packedMissing)
    # # print('packedMissing size: ', sys.getsizeof(packedMissing))
    # # print('packedMissing len: ', sys.getsizeof(packedMissing) * struct.calcsize('i'))
    # codefmt = len(b'missing')
    # intfmt = int((len(packedMissing) - codefmt) / struct.calcsize('i'))
    # print('bigger?: ', int((len(packedMissing) - codefmt) / struct.calcsize('i'))*struct.calcsize('i')+codefmt )
    # print('num of i', len(packedMissing) - len(b'missing'))
    # print('codefmt: ', codefmt, ' intfmt: ', intfmt)
    # unpackedMissing = struct.unpack('{}s{}'.format(codefmt, intfmt*'i'), packedMissing)
    # print(helpers.rawUnwrap(packedMissing))
    # print('unpackedMissing: ', unpackedMissing)
    # # print('dropped packets: ', missing)
    # print('')
    # print('received packets: ', len(helpers.receivedIndexes(tempFile)))
    print('')

    # helpers.verifyNumberOfChunks(tempFile, tempFile[0][1])
    # print(helpers.compareIndexes(tempFile))

    helpers.writeFile(tempFile, 'output', '.jpg')