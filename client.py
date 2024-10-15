from socket import *
import socket

HEADER = 64 
PORT = 5550
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname()) 
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(f"Connected with server on {SERVER}")

def send(msg):
    message = msg.encode(FORMAT)
    messageLength = len(message)
    sendLength = str(messageLength).encode(FORMAT)
    # to get the bytes but since I'm using numbers I might not need this
    sendLength += b' ' * (HEADER - len(sendLength)) 
    client.send(sendLength)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


while True:
    math_expression = input("Enter a math expression (or 0/0= to quit): ")
    send(math_expression)
    if math_expression == "0/0=":
        break

client.close()
