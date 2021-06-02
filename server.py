import threading
import socket

host = '127.0.0.1' #localhost
port = 55555 #port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #study it

server.bind((host, port)) #server is bound to host ip at the mentioned port

server.listen() #puts server to listening mode for incoming connections

clients = [] #connected clients will be stored
nicknames = [] #nicknames of connected clients

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)  # Broadcasting Messages
            broadcast(message)
        except:
            index = clients.index(index) #index of a failed client
            client.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def recieve():
    while True:
        # Accept Connectio
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == '__main__':
    print("Server is starting...[STARTED]")
    recieve()