import threading
import time
import socket
import numpy as np
from numpy import random

# initialize client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect client to our port
client.connect(('localhost', 4408))
print('The client has been connected')

print('Continue to provide the messages to send to server...')

# getting user input and sending it with the encoding format utf8

x = random.randint(100, size=5)
y = random.randint(100, size=5)

print(x)
print(y)

shapeX = x.shape[0]
shapeY = y.shape[0]
shapeStr = f"({shapeX},{shapeY})"

while True:
    msg = input('Please write the message (string in quotes):')
    client.send(bytes(msg, encoding='utf8'))

    #send shape info
    client.send(bytes(shapeStr, encoding='utf8'))

    #send array data
    client.sendall(x.tobytes())
    client.sendall(y.tobytes())