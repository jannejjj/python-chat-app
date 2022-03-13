import socket
import threading

#  Same basic connection as in the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 54321))

# Print instructions
print("Welcome to the chat application! Enter a nickname and type to chat\n"
      "Commands:\n"
      "/ch 1 - Switch to channel 1\n"
      "/ch 2 - Switch to channel 2\n"
      "/ch 3 - Switch to channel 3\n"
      "/main - Return to the main channel\n"
      "/w [nickname] - Sent a private whisper to the nickname specified \n"
      "/exit - Disconnect\n"
      )
#  Client has to input name first
nickname = input("Give a nickname: ")


#  Receives messages from server
def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')

            # Check if the received message is the codeword for sending the nickname
            if msg == "NAME_REQUEST":
                client.send(nickname.encode("utf-8"))

            # Check if received message is a whisper and has the client's name as the recipient
            elif '/w' in msg:
                if f'/w {nickname}' in msg:
                    # Looks weird here but the output is clean like this
                    print(f"Whisper received from {msg.replace(f'/w {nickname}', '')}")

            # Break loop when exiting
            elif '/exit' in msg:
                break

            # Print the received message normally
            else:
                print(">" + msg)
        except:
            print("You have been disconnected.")
            client.close()
            break


def write():
    while True:
        msg = f"{nickname}: {input('')}"
        client.send(msg.encode('utf-8'))
        if 'exit' in msg:
            client.send(msg.encode('utf-8'))
            break


receiver_thread = threading.Thread(target=receive)
receiver_thread.start()

writer_thread = threading.Thread(target=write)
writer_thread.start()