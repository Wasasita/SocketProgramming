from socket import *
import socket
import threading

# amount of bytes for the messages that the server will receive
HEADER = 64 
# anything above 5000 is safe 
PORT = 5550 
# get's IP address name of PC where it's running
SERVER = socket.gethostbyname(socket.gethostname()) 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #(family,type)
server.bind(ADDR)

def calculate(expression):
    try:
        # Remove the '=' sign and split the expression by operator
        expression = expression.replace("=", "").strip()
        if '+' in expression:
            x, y = expression.split('+')
            return str(float(x) + float(y))
        elif '-' in expression:
            x, y = expression.split('-')
            return str(float(x) - float(y))
        elif '*' in expression:
            x, y = expression.split('*')
            return str(float(x) * float(y))
        elif '/' in expression:
            x, y = expression.split('/')
            if float(y) == 0:
                if float(x) == 0:
                    return "Error: This is invalid, If you are trying to disconnect remember the ="
                return "Error: Division by zero"
            return str(float(x) / float(y))
        else:
            return "Error: Invalid operator"
    except:
        return "Error: Invalid input"

def handleClient(conn, addr):
    # print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        messageLength = conn.recv(HEADER).decode(FORMAT)
        if messageLength:
            messageLength = int(messageLength)
            message = conn.recv(messageLength).decode(FORMAT)

            # disconnect client from server automatically
            if message == "0/0=":
                print(f'Received question "{message}"; end the server program')
                conn.send("User input ends; end the client program".encode(FORMAT))
                connected = False
                break
            else:
                # print(f"[{addr}] {message}")
                result = calculate(message)
                print(f'Received question "{message}"; send back answer {result}')
                conn.send(result.encode(FORMAT))

            # blocker, receive specific message from client by measuring bytes
            # msg = conn.recv() 
    # conn.close()
    server.close()

def start():
    server.listen()
    print(f"Connected by client on {SERVER}")
    while True:
        # blocker type of message so no extra clients enter
        conn, addr = server.accept() 
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        # print(f"[active conncetions]{threading.active_count()-1}")

start()
