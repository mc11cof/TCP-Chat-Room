import socket, threading

#Prompting the client to enter a nickname 
nickname = input("Choose a nickname: ")

#Defining the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect client to localhost and port
client.connect(('127.0.0.1', 55555))

#Defining the receive function that will receive all the messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print (message)
        except:
            print("An error occurred!")
            client.close()
            break

#Defining the write function that will be use to send the messages of the client to the server            
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))
 
 
#Making threads so that the client can send and receive messages simultaneously       
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
            