#import socket module

#from thread import Thread


import thread

from socket import *

portNumber=15551

SocketPort = socket(AF_INET, SOCK_STREAM)

SocketPort.bind(('',portNumber))

SocketPort.listen(1)

print 'the web server is up on port:',portNumber


#********* PROXY_THREAD FUNC *************** #

def proxy_thread(connectionSocket, addr):



    # get the request from browser

    req = connectionSocket.recv(8192)
   
    

    # parse the first line

    firstline = req.split('\n')[0]

    # get url

    url = firstline.split(' ')[1]

    print 'URL :', url


    # find the webserver and port

    http_position = url.find("://")          # find pos of ://

    if (http_position==-1):

        temp = url

    else:

        temp = url[(http_position+3):]       # get the rest of url

    

    port_pos = temp.find(":")           # find the port pos (if any)



    # find end of web server

    webserver_pos = temp.find("/")

    if webserver_pos == -1:

        webserver_pos = len(temp)



    webserver = ""

    port = -1

    if (port_pos==-1 or webserver_pos < port_pos):      # default port

        port = 80

        webserver = temp[:webserver_pos]

    else:       # specific port

        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])

        webserver = temp[:port_pos]



    try:

        # create a socket to connect to the web server

        s = socket(AF_INET, SOCK_STREAM)  

        s.connect((webserver, port))

        s.send(req)         # send request to webserver

        

        while 1:

            # receive data from web server

            data = s.recv(8192)


            if (len(data) > 0):

                # send to browser

                connectionSocket.send(data)

            else:

                break

        s.close()

        connectionSocket.close()

    except socket.error, (value, message):

        if s:

            s.close()

        if connectionSocket:

            connectionSocket.close()

        print 'Runtime Error :', message 

        sys.exit(1)



while True:
    print 'Resdy to serve'
    connectionSocket, addr = SocketPort.accept()
    thread.start_new_thread( proxy_thread, (connectionSocket, addr))
        
        

			
