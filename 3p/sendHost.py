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

class Sender:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # self.s.setblocking(False)
    self.s.settimeout(0.1)
    self.ports = helpers.ports
    self.hostName = socket.gethostname()
    self.buffer = helpers.buffer
    self.chunkBytes = helpers.chunkBytes
    self.totalChunks = 0
    self.chunkSize = 0
    self.chunked = []
    self.unChunked = []
    self.missing = []
    self.filename = ''

    self.address = (self.hostName, self.ports['send'])
    self.proxy_address = self.hostName, self.ports['proxy']
    self.s.bind(self.address)

  def setFileName(self):
    self.filename = './send.jpg' #input('File path? (\'./filename.extension\' for current directory)')

  def initChunkValuesFromFile(self):
    self.chunkSize = helpers.getFileSize(self.filename)
    self.totalChunks = helpers.getNumChunks(self.filename)
  
  def readFile(self):
    i = 0
    with open(self.filename, 'rb') as f:
      while(True):
        bytesToSend = f.read(self.chunkBytes)
        #if you're done, leave / close the file
        if(not bytesToSend):
          f.close()
          break
        #makes an array of chunks in structs / converted to bytes
        self.chunked.append(helpers.wrapChunk(helpers.codes['sending'], i, self.totalChunks, bytesToSend))
        #this doesn't really need to go here, but it verifies that packed and unpacked structs are the same
        #i.e. that the bytes are correct
        self.unChunked.append(helpers.unwrapChunk(self.chunked[i]))
        #increments for the index of the chunk
        i += 1

  def sendFile(self):
    for chunk in self.chunked:
      self.s.sendto(chunk, self.proxy_address)
      # print(helpers.rawUnwrap(chunk))
      # time.sleep(0.0001)
      # print(i) # current chunk being sent
      # i += 1
      # print(chunk)
  def sendDone(self):
      self.s.sendto(helpers.codeWrap(helpers.codes['done']), self.proxy_address)

  def decision(self, data):
    if(helpers.codeUnwrap(data)[0] == helpers.codes['done']):
      #gather remaining
      print('done?')
    elif(helpers.codeUnwrap(data)[0] == helpers.codes['missing']):
      #retreive missing
      self.receiveMissing(data)
      self.sendDone()
      print('sending done')
    elif(helpers.codeUnwrap(data)[0] == helpers.codes['complete']):
      #stop
      print('complete?')
      sys.exit()

  def receiveMissing(self, data):
    # tempMissing = []
    print('test?????')
    if(data != [None]):
      # print('data: ', data)
      # print('recv miss: ', self.missing)
      self.missing.append(helpers.unwrapMissing(data))
      print('recv miss: ', self.missing[1:])
      self.sendMissing()
      self.missing = []

  def sendMissing(self):
    print('\n\nmissing: ', self.missing[0][1:])
    for i in self.missing[0][1:]:
      self.s.sendto(self.chunked[i], self.proxy_address)

    

try:
  sendHost = Sender()
  print(sendHost.proxy_address)
  print ('starting up on {}:{}'.format(sendHost.address[0], sendHost.address[1]))
  print ('connecting to {}:{}'.format(sendHost.proxy_address[0], sendHost.proxy_address[1]))

  sendHost.setFileName()
  sendHost.initChunkValuesFromFile()
  sendHost.readFile()
  sendHost.sendFile()
  print('sent file')
  # sendHost.sendDone()

  while(True):
    try:
      data, addr = sendHost.s.recvfrom(sendHost.buffer)
      sendHost.decision(data)

    except socket.timeout:
      try:
        if(sendHost.missing):
          sendHost.sendMissing()
        # print(sendHost.totalChunks)

        print('done?')

      except socket.timeout:
        print('timeout?')
    



finally:
  print('done')
