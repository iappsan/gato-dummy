import socket
from random import randrange

HOST = "192.168.1.107"      # El hostname o IP del servidor
PORT = 54321                # El puerto que usa el servidor
bufferSize = 1024           # Tamano del buffer

GAMESTATE = 0               # Estado actual del juego
GAMEDIFFICULT = 0           # Dificultad del juego
TABLES = [[                 # Tableros
            [' ','A','B','C'],
            ['1','-','-','-'],
            ['2','-','-','-'],
            ['3','-','-','-']
        ], [
            [' ','A','B','C','D','E'],
            ['1','-','-','-','-','-'],
            ['2','-','-','-','-','-'],
            ['3','-','-','-','-','-'],
            ['4','-','-','-','-','-'],
            ['5','-','-','-','-','-']
        ]]
GAMETABLE = TABLES[1]       # Inicializa un tablero

def validPos(throwPos, playerChar):      # Verifica si la posicion es valida
    convertedPos = ""
    if throwPos[0].isdigit():
        convertedPos = throwPos[0]
    else:
        if throwPos[0] == "A":
            convertedPos = '1'
        elif throwPos[0] == "B":
            convertedPos = '2'
        elif throwPos[0] == "C":
            convertedPos = '3'
        elif throwPos[0] == "D":
            convertedPos = '4'
        elif throwPos[0] == "E":
            convertedPos = '5'
        else:
            return False
    
    if GAMETABLE[convertedPos][throwPos[1]] == '-':
        GAMETABLE[convertedPos][throwPos[1]] = playerChar
        return True
    else:
        return False

def pcThrow():                          # Genera un tiro aleatorio
    ready = False
    if GAMEDIFFICULT == 1:
        size = 4
    else:
        size = 6
    while ready == False:
        randStr = str(randrange(1,size)) + str(randrange(1,size))
        ready = validPos(randStr, 'o')

def gameFinished(char2check):           # Se verifican las lineas
    size = 0
    i = 1
    j = 1
    if GAMEDIFFICULT == 1:
        size = 4
    else:
        size = 6

    while i < size:
        if GAMETABLE[i][j] == char2check:
            j+=1
        else:
            i+=1
            j=1
        if j == size:
            return True

    i = 1
    while i < size:
        if GAMETABLE[j][i] == char2check:
            j+=1
        else:
            i+=1
            j=1
        if j == size:
            return True

    i = 1
    j = 1
    while i < size:
        if GAMETABLE[i][j] == char2check:
            i+=1
            j+=1
    if i == size:
        return True
    
    i = 1
    j = 3
    while i < size:
        if GAMETABLE[i][j] == char2check:
            i+=1
            j-=1
    if i == size:
        return True
    else:
        return False

with  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor UDP activo, esperando peticiones")

    # Listen for incoming datagrams
    msgFromServer = "Bienvenido al Gato Dummy :)"
    stateStr = ""
    winnerStr = ""
    againStr = ""
    THROWCOUNTER = 0
    bytesToSend = str.encode(msgFromServer)

    while (GAMESTATE == 0):         # En espera de cliente
        data,address = UDPServerSocket.recvfrom(bufferSize)
        UDPServerSocket.sendto(bytesToSend, address)
        stateStr = "Escribe la cordenada de tu siguiente tiro"
        againStr = "Juegas de nuevo?\n(1)Si\n(2)No"
        THROWCOUNTER = 0
        GAMESTATE = 1

        while GAMESTATE == 1:       # Preguntando por dificultad
            UDPServerSocket.sendto(str.encode("Elige dificultad\n(1) Normal\n(2) Avanzado"), address)
            gd_data,address = UDPServerSocket.recvfrom(bufferSize)

            if gd_data == 1:
                GAMEDIFFICULT = 1
                GAMESTATE = 2
                THROWCOUNTER = 5
                GAMETABLE = TABLES[0]
            elif gd_data == 2:
                GAMEDIFFICULT = 2
                GAMESTATE = 2
                THROWCOUNTER = 13
                GAMETABLE = TABLES[1]
        
        while GAMESTATE == 2:       # Desarrollo del juego
            if THROWCOUNTER > 0:
                UDPServerSocket.sendto(str.encode(stateStr), address)
                gt_data,address = UDPServerSocket.recvfrom(bufferSize)
                if validPos(gt_data, 'x'):
                    stateStr = "Escribe la cordenada de tu siguiente tiro"
                    if gameFinished('x'):
                        winnerStr = "Has ganado!\n"
                        GAMESTATE = 3
                    else:
                        THROWCOUNTER -= 1
                        pcThrow()
                        if gameFinished('o'):
                            winnerStr = "Te han ganado!\n"
                            GAMESTATE = 3
                else:
                    stateStr = "No puedes tirar ahi\nElige un nuevo lugar"
            else:
                winnerStr = "Empate! Ya no quedan mas tiros\n"
                GAMESTATE = 3

        while GAMESTATE == 3:       # Quieres jugar de nuevo?
            againStr = winnerStr + againStr;
            UDPServerSocket.sendto(str.encode(againStr), address)
            ng_data,address = UDPServerSocket.recvfrom(bufferSize)

            if ng_data == 1:
                GAMESTATE = 1
            elif ng_data == 2:
                GAMESTATE == 0