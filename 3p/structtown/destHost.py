#CS 381 Networking Project 3 - rcvHost.py
#Michael Polston, Austin Little
#Receiving host for proxy
#

import socket
import sys
import helpers







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

file = []
tempData = None

i = 0
j = 0

while(True):
  try:
    # print(file)
    
    while(True):

      # data, addr = s.recvfrom(buffer)
      # file = [None]*helpers.decodeDict(data)['Total']

      while(True):
        data, addr = s.recvfrom(buffer)
        # if(i == 0):
          
        i += 1 
        j+=1
        
        if(data.decode('utf-8') == '&&$$__!!##@@'): #not data
          print('you done son, come at me with another one')
          #f.close()
          sys.exit() #close the program
          break
        
        file.append(helpers.decodeDict(data))
        # print(file[i-1]['chunk'].encode('ISO-8859-1'))

  finally:
      print('closing connection')
      print('')
      print('')
      print('')
      print(helpers.receivedIndexes(file))
      print('')
      print('')
      print('dropped packets: ', len(helpers.missingIndexes(file)))
      print('')
      print('')
      print('')
      print('')
      print('received packets: ', len(helpers.receivedIndexes(file)))
      print('')
      print('')
      print('')
      print('')
      # print(file[1])
      helpers.compareIndexes(file)
      helpers.verifyChunks(file, file[0]['Total'])
      helpers.writeFile(file)
      s.close() #close socket


# while(True):
#     #wait for connection
#   try:
#     #keep trying, one day you will get a file
#     #data is a <buffer> sized chunk, addr is where it's coming from
#     # data, addr = s.recvfrom(buffer)
#     # file = [None]*helpers.decodeDict(data)['Total']
#     print(file)
    
#     while(True):
#       #if the data you got is 'y'
#       ##if(data.decode('utf-8') == 'y'):
#         #open up a file named the thing below this
#       # f = open('receive.jpg', 'wb')
#       #I think these were here?
#       data, addr = s.recvfrom(buffer)
#       file = [None]*helpers.decodeDict(data)['Total']
#       # print(file)
#       # file = [None]*helpers.decodeDict(data)['Total'] #the issue is that this has to run for the dest to know
#         #keep going until you got the whole thing     #how big the file array needs to be
#       while(True):
#         #get more <buffer> sized chunks
#         # if(i == 0):
#         #   file = [None]*helpers.decodeDict(data)['Total']
#         data, addr = s.recvfrom(buffer)               #and it's ran again here, I'm assuming the first one is to get the 'y'
#         i += 1 
#         j+=1#so, this one would be where the file =bullshit*size would go, I guess
#         #if ur done                                   #but, it has to only run once if(i == 0)?
#                                                 #'y' validation has been removed for now, until we know its working then I can guess we can do that?
#                                                       #not necessary though, it can just listen indefinitely. prompting can be handled on sender side.
#         #TODO: don't keep that second part, I just wanted it to stop hanging
#         if(data.decode('utf-8') == '&&$$__!!##@@'): #not data
#           print('you done son, come at me with another one')
#           #f.close()
#           sys.exit() #close the program
#           break

#         #if data isn't empty print nonsense
#         # print(data, ' i: ', i)
#         #stack bytes ontop of what you already have until you get a file
#         # if(data):
#         #   print(data)
#           # file.insert(helpers.decodeDict(data)['#'], helpers.decodeDict(data))
#           #helpers.decodeDict(data) #problem child - When commented out all 6288 packets reach destHost
#                                               #what about now? Also, I'm on discord.
#                                             # not a cpu issue either. ran on my desktop. peaks at 37% cpu and still hangs up
#           #print(tempData)
#         # print(tempData['#'])
#         # f.write(tempData['chunk'].encode())
#         # print(sys.getsizeof(data), ' ', tempData['chunk'])
#         # if(i%100 == 0):
#           # print(tempData['Total'])
#           #print(helpers.decodeDict(data))
#           #print('{} packets received'.format(j))     
#           # print(i)
#         #if(not tempData):
#         #  tempData = helpers.decodeDict(data)
#         #  file.insert(tempData['#'], tempData)
#         #tempData = None
#         # file.insert(tempData['#'], tempData)
#         file.insert(helpers.decodeDict(data)['#'], helpers.decodeDict(data))

#   finally:
#       print('closing connection')
#       print(helpers.receivedIndexes(file))
#       print('dropped packets: ', len(helpers.missingIndexes(file)))
      
#       print('received packets: ', len(helpers.receivedIndexes(file)))
#       s.close() #close socket