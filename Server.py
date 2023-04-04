# required imports
import socket
import threading
import time
import numpy as np

def addVectors(A, B):
    print("Original Vector A: ", A, "\n", "Original Vector B: ", B, "\n")
    addRes = np.add(A, B)
    print("Result of Addition of A and B: ", addRes, " \n")


def subVectors(A, B):
    print("Original Vector A: ", A, "\n", "Original Vector B: ", B, "\n")
    subRes = np.subtract(A, B)
    print("Result of Subtraction of A and B: ", subRes, "\n")

def mulVectors(A, B):
    print("Original Vector A: ", A, "\n", "Original Vector B: ", B, "\n")
    mulRes = np.multiply(A, B)
    print("Result of Multiplication of A and B: ", mulRes, "\n")


# initialize server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# configure server
server.bind(('localhost', 4408))
server.listen()

# global variables
connected_clients = []

def NewClientSocketHandler(client_socket, client_address):
    global connected_clients
    print(f'New client connected: {client_address}')
    connected_clients.append(client_socket)

    while True:
        # receive message from client
        msg = client_socket.recv(1024).decode('utf8')

        # receive shape info
        shapeBytes = client_socket.recv(1024)
        shapeStr = shapeBytes.decode('utf-8').strip()

        shapeStr = shapeStr[1:-1]
        shapeX, shapeY = shapeStr.split(',')
        shapeX, shapeY = int(shapeX), int(shapeY)

        # receive array data
        x_bytes = b''
        y_bytes = b''
        while len(x_bytes) < 4 * shapeX:
            x_bytes += client_socket.recv(4 * shapeX - len(x_bytes))
        x = np.frombuffer(x_bytes, dtype=np.int32)

        while len(y_bytes) < 4 * shapeY:
            y_bytes += client_socket.recv(4 * shapeY - len(y_bytes))
        y = np.frombuffer(y_bytes, dtype=np.int32)

        print(f'Received message from {client_address}: {msg}')
        print(f'Received shape from {client_address}: ({shapeX}, {shapeY})')
        print(f'Received array data from {client_address}: {x}, {y}')

        if msg == 'add':
            addVectors(x, y)
        elif msg == 'sub':
            subVectors(x, y)
        elif msg == 'mul':
            mulVectors(x, y)
        else:
            print('Invalid operation')



    client_socket.close()


while True:
    # accept incoming client connections
    client_socket, client_address = server.accept()
    # start new thread to handle client socket
    threading.Thread(target=NewClientSocketHandler, args=(client_socket, client_address)).start()