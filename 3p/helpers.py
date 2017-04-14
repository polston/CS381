#CS 381 Networking Project 3 - helpers.py
#Michael Polston, Austin Little
#Helpers For Sending Host, Receiving Host, an

import socket
import os
import time
import helpers
import math
import struct
import sys
from operator import itemgetter

codes = { 'sending': 10, 'missing': 20, 'done':30, 'complete': 50 }

buffer = 4096
chunkBytes = 256 #receiver shouldn't know about this before receiving the data
ports = { 'send': 3000, 'proxy': 3001, 'dest': 3002 }


#returns the size of the file in bytes
def getFileSize(file):
    return os.path.getsize(file)

#returns the number of chunks in a file, rounded up 1
def getNumChunks(file):
    return math.ceil(getFileSize(file)/chunkBytes)

#wraps index, total, and chunk into a C-byte-struct-thing
def wrapChunk(head, i, total, chunk):
    fmt = '<hii{}s'.format(len(chunk))
    new = struct.pack(fmt, head, i, total, chunk)
    return new

#unpacks chunk, technically does fuckall until the index and total are done in wrap
def unwrapChunk(chunk):
    #chunk size is calculated by subctracting the size of integer*2 from the total received chunk
    fmt = '<hii{}s'.format(len(chunk) - struct.calcsize('i')*2 - struct.calcsize('h'))
    new = struct.unpack(fmt, chunk)
    return new

#wraps only the 'header' short int into a packet
def codeWrap(chunk):
    fmt = '<h'
    return struct.pack(fmt, chunk)

#unwraps the 'header' short int from a packet
def codeUnwrap(chunk):
    fmt = '<h{}s'.format(len(chunk) - struct.calcsize('h'))
    return struct.unpack(fmt, chunk)

#wraps the array of missing chunks as integers into a struct
#to be sent
def wrapMissing(missing):
    missingChunks = []
    wrappedChunks = []
    
    #while the missing array isn't empty
    while(len(missing)):
        tempMissing = []
        missingSize = 0
        #for each index in missing
        for i in missing:
            #the attempt was to make it so that the byte size didn't
            #exceed the same space as the file reading buffer
            #although, I think the way I'm doing it is off, because the maximum
            #byte size is 291 here after it's been converted to bytes?
            if(missingSize > 256):
              break
            #put the current index into the temporary array which stores only
            #a few chunks (enough to stay inside of the buffer when converted to bytes)
            tempMissing.append(missing.pop())
            missingSize += 4
        #put the smaller list of chunks into a list of lists of chunks
        missingChunks.append(tempMissing)
        
    #for every group of missing chunks/indexes
    for i in missingChunks:
        #the format for packing the chunk is 
        # little endian, short int (the header), and the chunk itself(all of the integers in the list/chunk)
        fmt = '<h{}'.format(len(i)*'i')
        #wrap the chunk, and put it into a list of wrapped chunks
        wrap = struct.pack(fmt, helpers.codes['missing'], *i)
        wrappedChunks.append(wrap)
    return wrappedChunks

#unwraps a payload of an array of integers with a leading short int message
def unwrapMissing(missing):
    fmt = '<h{}'.format( int(len(missing)/ 4)*'i' )
    return struct.unpack(fmt, missing)

#verifies length of array is the same as the completed file's
def verifyNumberOfChunks(chunks):
    total = chunks[0][2]
    if(len(chunks) == total):
        return True
    else:
        return False

# should return list of missing indexes
def missingIndexes(chunks):
    missing = []
    for key in chunks:
        if(chunks[key] == None):
            missing.append(key)
    return missing

#returns the indexes received
def receivedIndexes(chunks):
    received = [index[1] for index in chunks]
    return received

#determines whether or not an object exists
def exists(it):
    return (it is not None)

#determines whether or not an object exists, redundent for readability
def notExists(it):
    return (it is None)

#returns an object with the indexes for matching matching and not-matching indexes
def compareChunks(arr1, arr2):
    diff = len(arr1[0]) - len(arr2[0][3])
    temp = []
    nottemp = []
    for i in range(0, len(arr1)):
        if(arr1[i][diff:] == arr2[i][3]):
            temp.append(i)
        else:
            nottemp.append(i)
    return {'Matching': temp, 'Not Matching': nottemp}

#sorts values of an array based on the [1] index
#the [1] index in this case is the order that the chunks
#go into in order to properly form the file
def sortChunks(chunks):
    sortedChunks = sorted(chunks, key=itemgetter(1))
    return sortedChunks

#returns the actual order of chunks from an array/dictonary
def getChunkOrder(chunks):
    other = []
    for i in range(0, len(chunks)):
        other.append(chunks[i][1])
    return other

#creates an array of length size, with each index being a sequential integer
def indexArray(size):
    temp = []
    for i in range(0, size):
        temp.append(i)
    return temp

#writes file from bytes
def writeFile(fileBytes, filename):
    #initializes bytes object to store file bytes
    temp = []
    for k, v in fileBytes.items():
        temp.append(v)

    test = indexArray(len(fileBytes))
    temp = sortChunks(temp)

    byteFile = b''
    # print(fileBytes[1][3])
    #concatenates all chunks into single byte object
    for i in range(len(fileBytes)):
        if(temp[i][1] != test[i]):
            print('faulty?: ', test[i], ' -- ', temp[i])
        byteFile += temp[i][3]

    #writes the byte object to file
    with open('./'+filename, 'wb') as f:
        f.write(byteFile)
    f.close()