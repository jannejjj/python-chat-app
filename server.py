import threading
import socket
host = "127.0.0.1"
port = 54321

# Basic internet TCP server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Arrays for clients, names and channels
clients = []
names = []
ch1 = []
ch2 = []
ch3 = []


# Sends received messages to all clients
def send_message(msg):
    for c in clients:
        c.send(msg)


# Sends received messages to clients in channel 1
def send_ch1(msg):
    for client in ch1:
        client.send(msg)


# Sends received messages to clients in channel 2
def send_ch2(msg):
    for client in ch2:
        client.send(msg)


# Sends received messages to clients in channel 3
def send_ch3(msg):
    for client in ch3:
        client.send(msg)


# Handles received messages from one client
def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            decoded = msg.decode('utf-8')
            i = clients.index(client)
            client_name = names[i]

            # ----------      Channel switching      ---------- #
            # Switch to channel 1
            if '/ch 1' in decoded:
                if client not in ch1:
                    ch1.append(client)      # Add to channel
                    if client in ch2:
                        ch2.remove(client)  # Remove from other channels
                    elif client in ch3:
                        ch3.remove(client)
                    print(f"Switched client {client_name} to channel 1.")
                    client.send("Switched to channel 1.".encode('utf-8'))
                    continue

            # Switch to channel 2
            elif '/ch 2' in decoded:
                if client not in ch2:
                    ch2.append(client)      # Add to channel
                    if client in ch1:
                        ch1.remove(client)  # Remove from other channels
                    elif client in ch3:
                        ch3.remove(client)
                    print(f"Switched client {client_name} to channel 2")
                    client.send("Switched to channel 2.".encode('utf-8'))
                    continue

            # Switch to channel 3
            elif '/ch 3' in decoded:
                if client not in ch3:
                    ch3.append(client)      # Add to channel
                    if client in ch1:
                        ch1.remove(client)  # Remove from other channels
                    elif client in ch2:
                        ch2.remove(client)
                    print(f"Switched client {client_name} to channel 3")
                    client.send("Switched to channel 3.".encode('utf-8'))
                    continue

            # Leave both channels
            elif '/main' in decoded:
                if client in ch1:
                    ch1.remove(client)
                if client in ch2:
                    ch2.remove(client)
                if client in ch3:
                    ch3.remove(client)
                client.send("Left from channels.".encode('utf-8'))

            # Disconnect client
            elif '/exit' in decoded:
                i = clients.index(client)
                clients.remove(client)
                client.close()
                client_name = names[i]
                send_message(f'{client_name} has left the server.'.encode('utf-8'))
                print(f'{client_name} has left the server.')
                names.remove(client_name)
                break

            # Send the message to appropriate channels
            else:
                if client in ch1:
                    send_ch1(msg)
                elif client in ch2:
                    send_ch2(msg)
                elif client in ch3:
                    send_ch3(msg)
                else:
                    send_message(msg)

        # This except block is executed when the client isn't connected anymore (try-block gives an error)
        # The client and its name is removed from lists and a message is broadcast to the other clients.
        except:
            i = clients.index(client)
            clients.remove(client)
            if client in ch1:
                ch1.remove(client)
            if client in ch2:
                ch2.remove(client)

            client.close()
            client_name = names[i]
            send_message(f'{client_name} has left the server.'.encode('utf-8'))
            names.remove(client_name)
            break


def receive():
    while True:
        client, address = server.accept()  # All clients are accepted

        print(f"A client from address {str(address)} connected")
        client.send('NAME_REQUEST'.encode('utf-8'))  # This will be a codeword to the client to send a name

        name = client.recv(1024).decode('utf-8')
        clients.append(client)
        names.append(name)
        print(f"Their name is: {name}")

        send_message(f"{name} has joined the server!".encode("utf-8"))  # Broadcast to clients that a client has joined

        # Multithreading to handle each connected client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


print("Server started!")
receive()
