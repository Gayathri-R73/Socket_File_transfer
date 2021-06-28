######################### RPi TO COMP ###########################

##CLIENT PROGRAM (to be executed in COMP)##

import socket                           # Import socket module

s = socket.socket()                     # Create a socket object
host = socket.gethostname()             # Get local(COMP) machine name
print(host)

host= 'X.X.X.X'                         # IP of RPi (CLIENT)
port = 12345                            # Reserve a port for your service.
s.bind((host, port))                    # Bind to the port
s.listen(5)                             # Now wait for client connection.
   
while True:
        
    c, addr = s.accept()                # Establish connection with client.
    print ('Got connection from', addr)
    l = c.recv(1024)
    f = open("Digit from Rpi.jpg","wb")
    while (l): 
        print ("Receiving...")
        f.write(l)
        l = c.recv(1024)
    f.close()
    print ("Done Receiving")
    c.send(('Thank you for connecting').encode('utf-8'))
    c.close()                           # Close the connection
    
##################################################################
