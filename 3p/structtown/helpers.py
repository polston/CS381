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

buffer = 4096
chunkBytes = 256 #receiver shouldn't know about this before receiving the data

#returns the size of the file in bytes
def getFileSize(file):
  return os.path.getsize(file)

#returns the number of chunks in a file, rounded up 1
def getNumChunks(file):
    return math.ceil(getFileSize(file)/chunkBytes)

#wraps index, total, and chunk into a C-byte-struct-thing
def wrapChunk(i, total, chunk):
    fmt = '{}s'.format(len(chunk))
    new = struct.pack(fmt, chunk)
    return new

#unpacks chunk, technically does fuckall until the index and total are done in wrap
def unwrapChunk(chunk):
    fmt = '{}s'.format(len(chunk))
    new = struct.unpack(fmt, chunk)
    return new[0]
    
#verifies length of array is the same as the completed file's
def verifyChunks(arr, total):
    print(len(arr), ' vs ', total)
    if(len(arr) == total):
        return True
    else:
        return False

# should return list of missing indexes
def missingIndexes(arr):
    temp = []
    print(len(arr))
    for i in range(0, len(arr)):
        val = arr[i]
        if val is None:#notExists(arr[i]):
            temp.append(i)
    return temp

def receivedIndexes(arr):
    temp = []
    for i in range(0, len(arr)):
        if exists(arr[i]):
            temp.append(i)
    return temp
    
def exists(it):
    return (it is not None)

def notExists(it):
    return (it is None)

#returns an object with the indexes for matching matching and not-matching indexes
def compareIndexes(arr1, arr2):
    temp = []
    nottemp = []
    for i in range(0, len(arr1)):
        # print('arr1: ', arr1[2])
        # print('arr2: ', arr2[i][0])
        if(arr1[i] == arr2[i]):
            temp.append(i)
        else:
            nottemp.append(i)
    return {'Matching': temp, 'Not Matching': nottemp}
