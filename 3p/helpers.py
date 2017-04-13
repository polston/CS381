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
# import io

codes = { 'sending': 10, 'missing': 20, 'done':30 }

buffer = 4096
chunkBytes = 256 #receiver shouldn't know about this before receiving the data

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
    # print('unchunk size: ', struct.calcsize('ii{}s'.format(len(chunk))))
    # print('chunk size:', sys.getsizeof(chunk))
    #the format is (integer, integer, chunk)
    #chunk size is calculated by subctracting the size of integer*2 from the total received chunk
    fmt = '<hii{}s'.format(len(chunk) - struct.calcsize('i')*2 - struct.calcsize('h'))
    new = struct.unpack(fmt, chunk)
    # print('unchunked: ', new)
    # print()
    return new

def codeWrap(chunk):
    fmt = '<h'
    return struct.pack(fmt, chunk)

def codeUnwrap(chunk):
    fmt = '<h{}s'.format(len(chunk) - struct.calcsize('h'))
    return struct.unpack(fmt, chunk)

#verifies length of array is the same as the completed file's
def verifyNumberOfChunks(chunks):
    total = chunks[0][1]
    print('# of chunks: ', len(chunks), ' vs expected total: ', total)
    if(len(chunks) == total):
        # print('# of indexes is equal to number of chunks')
        return True
    else:
        # print('# of indexes is not equal to number of chunks')
        return False

# should return list of missing indexes
def missingIndexes(chunks):
    print(chunks[0])
    index = indexArray(chunks[0][2])
    received = receivedIndexes(chunks)
    missing = list(set(index)- set(received))
    print({'# Missing': len(missing), '#': missing})
    return missing

#returns the indexes received
def receivedIndexes(chunks):
    received = [index[0] for index in chunks]
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
        print('arr1: ', arr1[i][diff:])
        print('arr2: ', arr2[i][3])
        print()
        if(arr1[i][diff:] == arr2[i][3]):
            temp.append(i)
        else:
            nottemp.append(i)
    
    return {'Matching': temp, 'Not Matching': nottemp}

def compareIndexes(chunks):
    index = indexArray(chunks[0][1])
    temp = []
    nottemp = []
    if(verifyNumberOfChunks(chunks) == False):
        return 'Number of chunks inconsistent'
    for i in range(0, len(index)):
        # print('index: ', index[i])
        # print('chunk: ', chunk[i][0])
        if(index[i] == chunks[i][0]):
            temp.append(i)
        else:
            nottemp.append(i)
    return {'Matching': temp, 'Not Matching': nottemp}

def indexArray(size):
    temp = []
    for i in range(0, size):
        temp.append(i)
    return temp

def writeFile(bytes, filename, extention):
    #initializes bytes object to store file bytes
    byteFile = b''
    #concatenates all chunks into single byte object
    for chunk in bytes:
        byteFile += chunk[3]
    
    #writes the byte object to file
    with open('./'+filename+extention, 'wb') as f:
        f.write(byteFile)
    f.close()