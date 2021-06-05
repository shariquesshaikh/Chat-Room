import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")
n = len(nickname)

if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1' #localhost
port = 55555 #port
client.connect((host, port))

stop = False

# Listening to Server and Sending Nickname
def receive():
    while True:
        global stop
        if stop:
            break

        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_msg = client.recv(1024).decode('ascii')
                if next_msg == 'PASSWORD':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSED':
                        print("Invalid Credentials. Retry... ")
                        stop = True
                elif next_msg == 'BAN':
                    print("Connection refused because you are banned from the chat room!")
                    stop = True
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        if stop:
            break
        message = f'{nickname}: {input("")}'
        # global n
        offset = n + 2
        if message[offset:].startswith('/'):
            if nickname == 'admin':
                if message[offset:].startswith('/kick'):
                    client.send(f'KICK {message[offset+6:]}'.encode('ascii'))
                if message[offset:].startswith('/ban'):
                    client.send(f'BAN {message[offset+5:]}'.encode('ascii'))
            else:
                print('Commands can only be executed by admin.')
        else:
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()