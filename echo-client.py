import socket

HOST = "192.168.1.107"
PORT = 5432
BUFFERSIZE = 1024
mi_socket = socket.socket()
mi_socket.connect((HOST, PORT))

def main():

    while True:
        respuesta = mi_socket.recv(BUFFERSIZE).decode('UTF-8')
        print (respuesta)
        inputStr = input()
        mi_socket.send(str.encode(inputStr))

    mi_socket,close()

if __name__ == '__main__':
    main()