import socket

HOST = "192.168.1.107"
PORT = 5432
mi_socket = socket.socket()
mi_socket.bind((HOST, PORT))
mi_socket.listen(5)

while True:
    conexion, addr = mi_socket.accept()
    print ("Nueva conexion!")
    print (addr)

    conexion.send(str.encode("Hola desde del server"))
    conexion.close()