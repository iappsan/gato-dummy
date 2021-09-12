import socket

HOST = "192.168.1.107"
PORT = 5432
BUFFERSIZE = 1024
mi_socket = socket.socket()
mi_socket.connect((HOST, PORT))

mi_socket.send(str.encode("Hola esta es una prueba"))
respuesta = mi_socket.recv(BUFFERSIZE).decode('UTF-8')

print (respuesta)
mi_socket.close()