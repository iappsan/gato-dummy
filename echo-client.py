import socket

HOST = "192.168.1.114"  # El hostname o IP del servidor
PORT = 54321  # El puerto usado por el servidor

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = (HOST, PORT)
bufferSize = 1024

# Crea un socket UDP del lado del cliente

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
    # Enviando mensaje al servidor usando el socket UDP
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print("Message from Server {}".format(msgFromServer[0]))