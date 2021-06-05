import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")
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
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()