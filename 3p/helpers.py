#half of these are probably not doing anything
import socket
import os
import time
import helpers
import math
import json
import binascii
import pickle
import codecs
import base64
import struct
import sys
from operator import itemgetter
# import io

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
    # print('chunked: ', new)
    return new

#unpacks chunk, technically does fuckall until the index and total are done in wrap
def unwrapChunk(chunk):
    #chunk size is calculated by subctracting the size of integer*2 from the total received chunk
    fmt = '<hii{}s'.format(len(chunk) - struct.calcsize('i')*2 - struct.calcsize('h'))
    new = struct.unpack(fmt, chunk)
    # print('unchunked: ', new)
    return new

def codeWrap(chunk):
    fmt = '<h'
    return struct.pack(fmt, chunk)

def codeUnwrap(chunk):
    fmt = '<h{}s'.format(len(chunk) - struct.calcsize('h'))
    return struct.unpack(fmt, chunk)
    # temp = chunk[:2]
    # print('\n\n\nchunk: ', chunk)
    # fmt = '<h'
    return struct.unpack(fmt, chunk)

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
        # print('\n\nmissing chunk: ',i)
        #the format for packing the chunk is 
        # little endian, short int (the header), and the chunk itself(all of the integers in the list/chunk)
        fmt = '<h{}'.format(len(i)*'i')
        #wrap the chunk, and put it into a list of wrapped chunks
        wrap = struct.pack(fmt, helpers.codes['missing'], *i)
        print('wrap: ', wrap)
        print('fmt: ', fmt)
        wrappedChunks.append(wrap)
    return wrappedChunks

def unwrapMissing(missing):
    fmt = '<h{}'.format( int(len(missing)/ 4)*'i' )
    print('fmt: ', fmt)
    # print('fmt len?: ', int( ((len(missing)) - struct.calcsize('h')) / struct.calcsize('i')))
    # print('missing: ', missing)
    # print('fmt size?: ', (sys.getsizeof(missing) - struct.calcsize('h'))/4 )
    return struct.unpack(fmt, missing)

#verifies length of array is the same as the completed file's
def verifyNumberOfChunks(chunks):
    total = chunks[0][2]
    print('# of chunks: ', len(chunks), ' vs expected total: ', total)
    if(len(chunks) == total):
        # print('# of indexes is equal to number of chunks')
        return True
    else:
        # print('# of indexes is not equal to number of chunks')
        return False

# should return list of missing indexes
def missingIndexes(chunks):
    # print(chunks[0])
    missing = []
    for key in chunks:
        # missing = []
        if(chunks[key] == None):
            # print('key: ', key)
            missing.append(key)
    print('missing indexes: ', missing)
    return missing

#returns the indexes received
def receivedIndexes(chunks):
    received = [index[1] for index in chunks]
    # print({'# Received': len(received), '#': received})
    return received
    
def exists(it):
    return (it is not None)

def notExists(it):
    return (it is None)

#returns an object with the indexes for matching matching and not-matching indexes
def compareChunks(arr1, arr2):
    diff = len(arr1[0]) - len(arr2[0][3])
    temp = []
    nottemp = []
    for i in range(0, len(arr1)):
        # print('arr1: ', arr1[i][diff:])
        # print('arr2: ', arr2[i][3])
        # print()
        if(arr1[i][diff:] == arr2[i][3]):
            temp.append(i)
        else:
            nottemp.append(i)
    
    return {'Matching': temp, 'Not Matching': nottemp}

def sortChunks(chunks):
    sortedChunks = sorted(chunks, key=itemgetter(1))
    # otherthing = []
    # # print('\n\nthing: ',thing)
    # for i in thing:
    #     otherthing.append(i[1])
    # print('oteherthing: ',otherthing)
    return sortedChunks

def getChunkOrder(chunks):
    other = []
    # print(chunks)
    for i in range(0, len(chunks)):
        other.append(chunks[i][1])
        # print(i)
    print('asdfswaf')
    return other


# def compareIndexes(chunks):
    # index = indexArray(chunks[0][2])
    # temp = []
    # nottemp = []
    # # print('sorted?: ', sortAbomination(chunks))
    # # print('hello?')
    # if(verifyNumberOfChunks(chunks) == False):
    #     return 'Number of chunks inconsistent'
    # for i in range(0, len(index)):
    #     # print('index: ', index[i], ' - chunk: ', chunks[i][1], ' - ', index[i] == chunks[i][1])
    #     # print('chunk: ', chunk[i][1])
    #     if(index[i] == chunks[i][1]):
    #         temp.append(i)
    #     else:
    #         nottemp.append(i)
    # # print({'Matching': temp, 'Not Matching': nottemp})
    # if(nottemp):
    #     return False
    # else:
    #     return True
    # for 


def indexArray(size):
    temp = []
    for i in range(0, size):
        temp.append(i)
    # print(temp)
    return temp

# def removeUnneededChunks(chunks):
#     temp = chunks
#     for i in range(0, chunks[0][1]):
        
#     return temp

def writeFile(fileBytes, filename, extension):
    #initializes bytes object to store file bytes
    temp = []
    for i in fileBytes:
        temp.append(i)

    temp = sortChunks(temp)

    byteFile = b''
    # print(fileBytes[1][3])
    #concatenates all chunks into single byte object
    for i in range(len(fileBytes)):
        print(temp[i])
        byteFile += temp[i][3]
    
    #writes the byte object to file
    with open('./'+filename+extension, 'wb') as f:
        f.write(byteFile)
    f.close()