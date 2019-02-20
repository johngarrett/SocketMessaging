#John Garrett 
# 2 - 18 - 2019

import selectors
import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

#accept incoming connections
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'') #hold the daata we want along with the socket
    events = selectors.EVENT_READ | selectors.EVENT_WRITE 
    sel.register(conn, events, data=data) #pass over events mask, socket, and data objects

#handle client connection
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: #if the socket is ready to read, both will be true 
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]    #store the bytes sent

#handle incorrect usage (no specified host and port num)
if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False) #config the socket in non-blocking mode
sel.register(lsock, selectors.EVENT_READ, data=None) #registers the socket to be monitored

try:
    while True:
        events = sel.select(timeout=None) #blocks until there are sockets ready
        for key, mask in events:
            #if the key is none, we know its an unaccpeted connection; accept it
            if key.data is None:
                accept_wrapper(key.fileobj)
            #if it has already been selected, service the connection
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()