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

class Destination:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # self.s.setblocking(False)
    self.s.settimeout(0.1)
    self.ports = helpers.ports
    self.hostName = socket.gethostname()
    self.buffer = helpers.buffer
    self.chunkBytes = helpers.chunkBytes
    self.tempFile = []
    self.pendingFile = {}
    self.missing = []
    self.missingChunks = []
    self.address = (self.hostName, self.ports['dest'])
    self.proxy_address = self.hostName, self.ports['proxy']
    self.s.bind(self.address)
    self.madeSkeleton = False
  
          
  #puts the missing chunk indexes into an array
  def getMissing(self):
    # print('asdfsadfadfasdf')
    # self.missing = helpers.missingIndexes(self.tempFile)
    self.missing = helpers.missingIndexes(self.pendingFile)
    # print(helpers.missingIndexes(self.tempFile))
    # print('missing:', self.missing)
    self.missingChunks = helpers.wrapMissing(self.missing)
    # print('missing chunks: \n', self.missingChunks)
    # self.missing = []
    # print('\nmissing: ', self.missing)
    # print('\nmissingchunks: ', self.missingChunks)

  #puts the received chunks into an array
  def addToFile(self, chunk):
    self.tempFile.append(helpers.unwrapChunk(chunk))
    # print('tempFile: ', self.tempFile)
    for temp in self.tempFile:
      
      if(self.pendingFile.get(temp[1]) == None):
        # print('temp1: ', temp[1])
        self.pendingFile[temp[1]] = temp
    # self.tempFile = []

  def fileSkeleton(self):
    # print(helpers.indexArray(self.tempFile[0][2]))
    temp = list(helpers.indexArray(self.tempFile[0][2]))
    # for i in temp:
    #   temp[i] = str(i)
    for i in temp:
      self.pendingFile[i] = None

  #sends missing chunks to the proxy
  def sendMissing(self):
    for i in self.missingChunks:
      self.s.sendto(i, self.proxy_address)
    self.missingChunks = []
  
  def sendWaiting(self):
    self.s.sendto(i, self.proxy_address)
  
  def sendComplete(self):
    self.s.sendto(helpers.codeWrap(helpers.codes['complete']), self.proxy_address)

  def decision(self, data):
    if(helpers.codeUnwrap(data)[0] == helpers.codes['sending']):
      # print('received sending')
      self.addToFile(data)
      # print('pending file length?:', len(self.pendingFile), ' expected length?: ', self.tempFile[0][2])
    elif(helpers.codeUnwrap(data)[0] == helpers.codes['complete']):
      #stop
      print('complete?')
  
  def fileReady(self):
    # print('pending file length?:', len(self.pendingFile), ' expected length?: ', self.tempFile[0][2])
    for chunk in self.pendingFile:
      if(self.pendingFile[chunk] == None):
        print('missing chunk: ', chunk)
        return False
    return True
  
  def countValues(self):
    counter = 0
    value = 0
    for i in range(0, len(self.pendingFile)):
      print('counter: ', counter, ' value: ', len(self.pendingFile[i][3]))
      # print('v: ', v)
      counter += 1
    print(counter)
  


destHost = Destination()

while(True):
  start = time.time()
  try:
    data, addr = destHost.s.recvfrom(destHost.buffer)
    destHost.decision(data)
    # print(data)

    if(destHost.madeSkeleton is False):
      destHost.fileSkeleton()
      # print(destHost.pendingFile)
      destHost.madeSkeleton = True

  except socket.timeout:
    if(destHost.fileReady() == False):
      destHost.getMissing()
      destHost.sendMissing()
      # destHost.missingChunks = []
      # print(destHost.pendingFile)

    # if(not destHost.missing or not destHost.missingChunks):
      
      
    elif(destHost.pendingFile):
      # destHost.tempFile = helpers.removeUnneededChunks(destHost.tempFile)
      # print('pls', helpers.verifyNumberOfChunks(destHost.tempFile), ' - ', helpers.compareIndexes(destHost.tempFile))
      # print(destHost.pendingFile)
      if(destHost.fileReady() == True): # if(helpers.verifyNumberOfChunks(destHost.tempFile) and helpers.compareIndexes(destHost.tempFile)):
        print('asdfasdf')
        destHost.countValues()
        print(destHost.pendingFile[20])
        destHost.sendComplete()
        helpers.writeFile(destHost.tempFile, 'test', '.jpg')
        break