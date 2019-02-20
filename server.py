
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#handle incoming clients 
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

#handle a single client connection
def handle_client(client):  
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
       msg = client.recv(BUFSIZ)
       if msg != bytes("{quit}", "utf8"):
           broadcast(msg, name+": ")
       else:
           client.send(bytes("{quit}", "utf8"))
           client.close()
           del clients[client]
           broadcast(bytes("%s has left the chat." % name, "utf8"))
           break

#send a message to all connected clients
def broadcast(msg, prefix=""):  # prefix is for name identification.
     for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

if __name__ == "__main__":
    HOST = input("Host (default is 127.0.0.1): ")
    PORT = input("Port (default is 33000): ")
    _max = int(input("Max connections: "))
    SERVER.listen(_max) 
    print("Waiting for a connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() #start the loop
    ACCEPT_THREAD.join() 
    SERVER.close()