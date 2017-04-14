#CS 381 Networking Project 3 - destHost.py
#Michael Polston, Austin Little
#Receiving Host For Gremlin Proxy
# This is the destination host for the gremlin proxy/sending host. This host will receive packets from the proxy, unpack them, and then store them
# in an array. The sequence numbers are then checked to verify which packets are actually missing, and then requests will be sent to the proxy, which 
# will then be forwarded to the sending host. The sending host will then resend the packets that the destination requested, and so on and so forth.
# This will continue until every packet has arrived, and then they are written to a file.

#import statements
import socket
import sys
import helpers
import time
import io
import struct
import math


class Destination:
  #the __init__ for destination is largely the same as sender
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
    self.madeSkeleton = False #whether or not a dictionary of chunks has been created
  
          
  #puts the missing chunk indexes into an array
  def getMissing(self):
    #finds missing indexes from the skeleton/pending file
    self.missing = helpers.missingIndexes(self.pendingFile)
    #wraps missing indexes into packets to be sent
    self.missingChunks = helpers.wrapMissing(self.missing)

  #puts the received chunks into an array
  def addToFile(self, chunk):
    self.tempFile = []
    self.tempFile.append(helpers.unwrapChunk(chunk))
    for temp in self.tempFile:
    # for key in self.pendingFile.keys():
      #places it into the skeleton if there is currently no chunk in that key:value
      # if(self.pendingFile.get(0) != None):
      #   print(self.pendingFile.get(0))
      #   sys.exit()
      if(self.pendingFile.get(temp[1]) == None):
        self.pendingFile[temp[1]] = temp
  
  #initializes the skeleton of how many chunks will compose the file
  def fileSkeleton(self):
    temp = list(helpers.indexArray(self.tempFile[0][2]))
    for i in temp:
      self.pendingFile[i] = None

  #sends missing chunks to the proxy
  def sendMissing(self):
    for i in self.missingChunks:
      self.s.sendto(i, self.proxy_address)
    self.missingChunks = [] #clears missing chunk cache
  
  #sends sentinel value to the sender
  def sendComplete(self):
    self.s.sendto(helpers.codeWrap(helpers.codes['complete']), self.proxy_address)

  #makes decision based on type of message received
  def decision(self, data):
    #if the message is a chunk being sent
    if(helpers.codeUnwrap(data)[0] == helpers.codes['sending']):
      self.addToFile(data)
  
  #if each key in the skeleton has the appropriate value
  #the file is ready to be written
  def fileReady(self):
    for chunk in self.pendingFile:
      if(self.pendingFile[chunk] == None):
        return False #if any value is empty
    return True #if all values are accounted for
  
  #count the number of values inside the dictionary
  def countValues(self):
    counter = 0
    value = 0
    for i in range(0, len(self.pendingFile)):
      if(self.pendingFile[i] != None):
        counter += 1
    return counter
  


destHost = Destination() #instantiate the destination
print('Waiting for connection.')

while(True):
  try:
    data, addr = destHost.s.recvfrom(destHost.buffer)
    destHost.decision(data) #make decision based on received packet message
    
    if(destHost.madeSkeleton is False): #if there is no skeleton yet
      destHost.fileSkeleton() #make skeleton
      destHost.madeSkeleton = True #don't make another skeleton

  except socket.timeout:
    if(destHost.fileReady() == False):
      #simple progress ticker
      print('progress: {:0.7f}%'.format( ( (destHost.countValues()/len(destHost.pendingFile)) *100 )))
      #if there was a timeout find out what you're missing
      destHost.getMissing()
      #send the missing indexes
      destHost.sendMissing()
      
    # check if the skeleton exists
    elif(destHost.pendingFile):

      #if the skeleton is full, i.e. the file is ready to be written
      if(destHost.fileReady() == True):
        print(destHost.countValues()) #was used for verificaton
        destHost.sendComplete() #send complete message to proxy and sender
        filename = input('Enter file name/path (with extension): ')
        print('Writing file')
        helpers.writeFile(destHost.pendingFile, filename) #writes the file
        print('File written')
        break