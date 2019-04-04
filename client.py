from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def receive():
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if msg == "/quit":
            client_socket.close()
            break
        if not msg:
            break
        print(msg)

def send():
    while True:
        msg = input()
        client_socket.send(bytes(msg, "utf8"))
        if msg == "/quit":
            break


HOST = input('Enter host(default is 127.0.0.1): ') or '127.0.0.1'
PORT = input('Enter port(default is 33000): ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()
