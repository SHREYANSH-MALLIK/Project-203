import socket

from threading import Thread

# socket.socket(address family , socket type)

# address family is the family of addresses that the socket can communicate with. Classic
# examples of 2 of the most famous address families are IPv4 and IPv6.
# AF_INET represents IPv4 while AF_INET6 represents IPv6.
# AF_INET is also the default value of the first argument, if not provided. That’s because
# IPv4 is still widely used while IPv6 is relatively new.

# we are using SOCK_STREAM. It is the default value (if not provided) and it
# is used to create a TCP Socket. We could also use SOCK_DGRAM which is used to
# create a UDP Socket, however use of it case specific.

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

ip_adress = "127.0.0.1"
port = 8000

server.bind((ip_adress,port))

server.listen()

clients = []
nicknames = []

print("Server is starting!!")


def clientThread(connected,nickname):
    connected.send("Welcome to the chat room".encode('utf-8'))
    while True: 
        try: 
            message = connected.recv(2048).decode('utf-8')
            if message:
                print(message)
                broadcast(message, connected)
            else :
                remove(connected)
                removeNickname(nickname)

        except :
            continue
        

def removeNickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)



def broadcast(message,connection):
    for c in clients : 
        if c != connection:
            try:
                c.send(message.encode('utf-8'))
            except:
                remove(c)
    

def remove(connection):
    if connection in clients :
        clients.remove(connection)


while True :
    connected,address = server.accept()
    
    connected.send("NICKNAME".encode("utf-8"))
    nickname = connected.recv(2048).decode("utf-8")

    clients.append(connected)
    nicknames.append(nickname)

    message = "{} joined!".format(nickname)
    print (message)