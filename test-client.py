import socket

HOST = "192.168.1.107"
PORT = 5432
BUFFERSIZE = 1024
mi_socket = socket.socket()
mi_socket.connect((HOST, PORT))

while True:
    inputStr = input()
    mi_socket.send(str.encode(inputStr))
    respuesta = mi_socket.recv(BUFFERSIZE).decode('UTF-8')
    print (respuesta)

mi_socket.close()