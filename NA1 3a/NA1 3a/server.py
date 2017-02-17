#import socket module
from socket import *
s_Socket = socket(AF_INET, SOCK_STREAM)
#prepare a server socket
s_Port = 45678
s_Socket.bind(('',s_Port))
s_Socket.listen(1)
while 1:
    print ('ready to go')
    conn_Socket, addr = s_Socket.accept()
    try:
        mg = conn_Socket.recv(1024)
        
        f_name = mg.split()[1]
        f = open(f_name[1:])
        o_data = f.read()
        conn_Socket.send('\nHTTP/1.x 200 OK\n')
        conn_Socket.send(o_data)
        for i in range(0, len(o_data)):
            conn_Socket.send(o_data[i])
        conn_Socket.close()
    except IOError:
        conn_Socket.send('\n404 File Not Found')  
    conn_Socket.close()
    
