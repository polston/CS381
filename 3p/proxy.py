import sys, socket, random, helpers #import system libraries and our helper file

#Get Ports of Sender, Proxy, and Receiver
sendPort = helpers.ports['send'] 
proxPort = helpers.ports['proxy']
destPort= helpers.ports['dest']

address = socket.gethostname() # get IP address
buffer = helpers.buffer # get buffer size

#Counter Variables for packet statistics
i=0
j=0 
k=0
g=0

#create a UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Build connections to other programs
proxy_address = (address, proxPort)
sendHost_address = (address, sendPort)
destHost_address = (address, destPort)

print ('starting up on {}:{}'.format(proxy_address[0], proxy_address[1]))
s.bind(proxy_address) #bind port

sendHost = sendHost_address
destHost = destHost_address

#Get drop rate from user
dropRate = input('Whats the drop rate of this proxy? (0-100)%\n')
print('The configured drop rate is: {}%'.format(dropRate)) #affirm drop rate
while True:
#wait for connection
  try:
    #keep trying, one day you will get a connection
    while(True):
      #get more <buffer> sized chunks
      data, addr = s.recvfrom(buffer)
      i+=1 #iterate packet total
      
      if(helpers.codeUnwrap(data)[0] == helpers.codes['complete']): #if receiver has all packets
        print('File Transfer Complete')
        s.sendto(data, sendHost) #signal sender
        sys.exit() #break loop
      print('Received Packet From {}'.format(addr))
      
      if(random.random()*100 > float(dropRate)): #generate a random number and compare against dropRate. if Greater, send packer
        if(addr[1] == sendHost_address[1]): # if packet is from sender
          print('Forwarding Packet To {}'.format(destHost))
          s.sendto(data, destHost) #send to destination
          k+=1 #iterate packet total
        elif(addr[1] == destHost_address[1]): #if packet is from destination
          print('Forwarding Packet To {}'.format(sendHost))
          s.sendto(data, sendHost) #send to sender
          g+=1 #iterate packet total
      else: #if random value doesn't meet threshold, drop packet
        print('Dropped Packet From:{}'.format(addr))
        j+=1 #iterate packet total
        
  finally: #file has been sent, print session statistics
      print('closing connection\n')
      print("--------------Connection Statistics: Sender to Destination--------------")
      print('{} forwarded packets'.format(k))
      print("--------------Connection Statistics: Destination to Sender--------------")
      print('{} forwarded packets'.format(g))
      print("--------------Connection Statistics: Total Packets and Drop Rate--------------")
      print('{} received packets'.format(i))
      print('{} dropped packets at a drop rate of {}%'.format(j,dropRate))
      print('Actual drop rate: {:0.2f}%'.format(((j/i)*100)))
      print('{} total forwarded packets\n'.format(k+g))
      s.close() #close socket