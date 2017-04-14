#CS 381 Networking Project 3 - sendHost.py
#Michael Polston, Austin Little
#Sending Host For Gremlin Proxy
# This is the sending host for the gremlin proxy/destination host. This host will read a user-entered file name from the local directory, and then
# convert that file to packets and send to the gremlin proxy. It also continously listens for incoming messages to know whether or not a packet needs to be
# resent. If it receives a resend request, it will only attempt to resend the missing packets request.

import socket
import os
import os.path
import time
import helpers
import sys
import io

class Sender:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creating socket
    # self.s.setblocking(False)
    self.s.settimeout(0.1) #setting timeout period, because sockets are blocking
    self.ports = helpers.ports #ports used for the proxy/sender/receiver
    self.hostName = socket.gethostname() #this hostname
    self.buffer = helpers.buffer #the buffer size for sending bytes
    self.chunkBytes = helpers.chunkBytes #the buffer size for reading bytes
    self.totalChunks = 0 #total number of packets the file is split into
    self.chunkSize = 0 #size of each individual packet
    self.chunked = [] #packets ready to be sent
    # self.unChunked = [] #unpacked packets, was used for testing verification
    self.missing = [] #received indexes of missing packets
    self.filename = '' #the name/path of the file to be sent

    self.address = (self.hostName, self.ports['send'])
    self.proxy_address = self.hostName, self.ports['proxy']
    self.s.bind(self.address)

  #sets the name of the file to be sent
  def setFileName(self):
    self.filename = input('File path? (\'./filename.extension\' for current directory): ')

  #initializes how many packets and how big they are
  def initChunkValuesFromFile(self):
    self.chunkSize = helpers.getFileSize(self.filename)
    self.totalChunks = helpers.getNumChunks(self.filename)
  
  #reads from the file and generates the 'chunked' array for sending
  def readFile(self):
    i = 0 #counts the index, put inside the packets for reference on both ends
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
        # self.unChunked.append(helpers.unwrapChunk(self.chunked[i]))
        #increments for the index of the chunk
        i += 1

  #initial sending of the file to the destination
  def sendFile(self):
    for chunk in self.chunked:
      self.s.sendto(chunk, self.proxy_address)
      
  def sendDone(self):
      self.s.sendto(helpers.codeWrap(helpers.codes['done']), self.proxy_address)

  #determines what to do depending on what sort of message it gets back
  #from the destinations
  def decision(self, data):
    if(helpers.codeUnwrap(data)[0] == helpers.codes['missing']):
      #retreive missing
      self.receiveMissing(data)
      self.sendDone()
      print('sending done')
    elif(helpers.codeUnwrap(data)[0] == helpers.codes['complete']):
      #stop
      print('received complete, exiting')
      sys.exit()
      
  #receives messages forwarded to it
  def receiveMissing(self, data):
    if(data != [None]): #if the data received actually contains something
      #unwrap packet and put received missing indexes into array
      self.missing.append(helpers.unwrapMissing(data)) 
      self.sendMissing() #send missing packets back over
      self.missing = [] #clear out the missing packets cache, so as to not resend them
  
  #sends missing packets queried from the destination
  def sendMissing(self):
    #prints how many file chunks/packets were requested
    print('{} chunks requested for transfer'.format(len(self.missing[0][1:])))
    #sends the missing chunks to the destination/proxy
    #the structure is unpacked as a tuple, and the first index is the message
    #so [0][1:] is the packet, and it starts reading from right after the packet message
    print(self.missing)
    for i in self.missing[0][1:]:
      self.s.sendto(self.chunked[i], self.proxy_address)

    

try:
  sendHost = Sender() #instantiates the sender
  print(sendHost.proxy_address)
  print ('starting up on {}:{}'.format(sendHost.address[0], sendHost.address[1]))
  print ('connecting to {}:{}'.format(sendHost.proxy_address[0], sendHost.proxy_address[1]))

  sendHost.setFileName() #establish file path
  sendHost.initChunkValuesFromFile() #establish how many packets
  sendHost.readFile() #read file into chunks
  sendHost.sendFile() #attempt to send entire file
  print('sent file')

  while(True):
    try:
      data, addr = sendHost.s.recvfrom(sendHost.buffer)
      sendHost.decision(data) #do something depending on the message received

    except socket.timeout:
        if(sendHost.missing): #if there are missing packets
          sendHost.sendMissing() #send missing packets

finally:
  print('done')
