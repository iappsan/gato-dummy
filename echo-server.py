import socket
from random import randrange

HOST = "192.168.1.107"      # El hostname o IP del servidor
PORT = 5432                 # El puerto que usa el servidor
BUFFERSIZE = 1024           # Tamano del buffer
MYSOCKET = socket.socket()  # Iniciamos el socket
MYSOCKET.bind((HOST, PORT)) # Lo ligamos al host y al puerto
MYSOCKET.listen(5)          # Definimos el numero de conecciones a escuchar
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

def tableToStr():                       # Convierte el tablero a cadena
    genStr = '\n'
    for i in range(len(GAMETABLE)):
        for j in range(len(GAMETABLE[i])):
            genStr = genStr + str(GAMETABLE[i][j]) +' '
        genStr = genStr + '\n'

    return str.encode(genStr)

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

def main():
    CONN, ADDR = MYSOCKET.accept()      # En espera de cliente
    print ("Nueva conexion!")
    print (ADDR)

    STATESTR = ""                       # Se inicializan valores para el juego
    WINNERSTR = ""
    AGAINSTR = ""
    THROWCOUNTER = 0
    
    while (GAMESTATE == 0):             # Bienvenida al gato dummy

        STATESTR = "Escribe la cordenada de tu siguiente tiro"
        AGAINSTR = "Juegas de nuevo?\n(1)Si\n(2)No"
        THROWCOUNTER = 0
        GAMESTATE = 1

        while GAMESTATE == 1:       # Preguntando por dificultad
            CONN.send(str.encode("Bienvenido al Gato Dummy :)\n"
                            +"Elige dificultad\n(1) Normal\n(2) Avanzado"))
            gd_data = int(CONN.recv(BUFFERSIZE).decode('UTF-8'))
            print("Dificultad elegida: "+ str(gd_data))

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
            else:
                gd_data = ""
        
        while GAMESTATE == 2:       # Desarrollo del juego
            if THROWCOUNTER > 0:
                CONN.send(str.encode(STATESTR))
                gt_data = CONN.recv(BUFFERSIZE).decode('UTF-8')

                if validPos(gt_data, 'x'):
                    STATESTR = "Escribe la cordenada de tu siguiente tiro"
                    if gameFinished('x'):
                        WINNERSTR = "Has ganado!\n"
                        GAMESTATE = 3
                    else:
                        THROWCOUNTER -= 1
                        pcThrow()
                        if gameFinished('o'):
                            WINNERSTR = "Te han ganado!\n"
                            GAMESTATE = 3
                else:
                    STATESTR = "No puedes tirar ahi\nElige un nuevo lugar"
            else:
                WINNERSTR = "Empate! Ya no quedan mas tiros\n"
                GAMESTATE = 3

        while GAMESTATE == 3:       # Quieres jugar de nuevo?
            AGAINSTR = WINNERSTR + AGAINSTR;
            CONN.send(str.encode(AGAINSTR))
            ng_data = int(CONN.recv(BUFFERSIZE).decode('UTF-8'))

            if ng_data == 1:
                GAMESTATE = 1
            elif ng_data == 2:
                GAMESTATE == 0

if __name__ == '__main__':
    main()