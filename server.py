import threading
import socket

host = '127.0.0.1' #localhost
port = 55555 #port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #study it

server.bind((host, port)) #server is bound to host ip at the mentioned port

server.listen() #puts server to listening mode for incoming connections

clients = [] #connected clients will be stored
nicknames = [] #nicknames of connected clients
banneduser = []
# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)  # Broadcasting Messages
            ifadmin = (False, True) [nicknames[clients.index(client)] == 'admin']
            
            if msg.decode('ascii').startswith('KICK'):
                if ifadmin:
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Admin role required to execute the command!').encode('ascii')
            elif msg.decode('ascii').startswith('BAN') and ifadmin:
                if ifadmin:
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Admin role required to execute the command!').encode('ascii')    
            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client) #index of a failed client
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break

# Receiving / Listening Function
def recieve():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname + '\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('PASSWORD'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'admin':
                client.send('REFUSED')
                client.close()
                continue
        
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))

if __name__ == '__main__':
    print("Server is starting...[STARTED]")
    recieve()