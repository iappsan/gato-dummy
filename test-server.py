import socket

HOST = "192.168.1.107"
PORT = 5432
mi_socket = socket.socket()
mi_socket.connect((HOST, PORT))

while True:
    conexion, addr = mi_socket.accept()
    print ("Nueva conexion!")
    print (addr)

    conexion.send("Hola desde del server")
    conexion.close()