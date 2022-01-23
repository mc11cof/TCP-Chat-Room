#Importing the modules needed
import threading
import socket

#Defining the host and port
host = '127.0.0.1' #localhost
port = 55555

#Start a server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the server to the localhost and the port
server.bind((host, port))

#Let the server listen for incoming connections
server.listen()

#Define a client and nicknames list that will be used to store all the clients connectected to the server as well as their username
clients = []
nicknames = []

#Defining a function that sends a messages to all the clients connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)


#Processing the messages sent by a client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

#Prompt a client once they connect and asking them for a nickname
def receive():
    while True: 
        client, address = server.accept()
        print("Connected with {str(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
print("Server is listening...")        
receive()       
        
