import socket

HOST = "192.168.1.107"
PORT = 5432
BUFFERSIZE = 1024
mi_socket = socket.socket()
mi_socket.bind((HOST, PORT))
mi_socket.listen(5)

conexion, addr = mi_socket.accept()
print ("Nueva conexion!")
print (addr)

while True:
    peticion = conexion.recv(BUFFERSIZE).decode('UTF-8')
    print (peticion)
    conexion.send(str.encode("Hola desde del server"))

conexion.close()