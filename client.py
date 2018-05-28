import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.102', 10000)
print("connecting to " + str(server_address))

try:
	sock.connect(server_address)
	print("Please input table number")
	tableNr = raw_input()
	print("Sending table nr: " + tableNr)
	sock.sendall(tableNr)
	time.sleep(10)


except socket.error, exc:
    print "Caught exception socket.error : %s" % exc

finally:
	print >>sys.stderr, 'closing socket'
	sock.close()  

