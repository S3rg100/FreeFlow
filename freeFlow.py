def initialize():  
    lineas = []
    with open("entradas\entrada2.txt", "r") as archivo:
        lineas = archivo.readlines()

    # Obtener el tamaño del tablero
    filas = int(lineas[0].split(",")[0])
    columnas = int(lineas[0].split(",")[1])

    # Crear el tablero vacío
    tablero = [[0 for _ in range(columnas)] for _ in range(filas)]

    # Diccionario para guardar las posiciones de cada número
    puntos = {}

    # Llenar el tablero y registrar los puntos
    for linea in lineas[1:]:
        fila, columna, numero = map(int, linea.strip().split(","))
        fila -= 1 
        columna -= 1

        tablero[fila][columna] = numero

        if numero not in puntos:
            puntos[numero] = [(fila, columna)]
        else:
            puntos[numero].append((fila, columna))

    return tablero, puntos


def printTablero (tablero):
    print("_______________________")
    for fila in tablero:
        print("|", " ".join(map(str, fila)), "|") 
    print("_______________________")
    

def seleccionar_numero_inicial(numeros_pendientes):
    numero_inicial = None

    while numero_inicial not in numeros_pendientes:
        try:
            numero_inicial = int(input("Ingrese el número inicial: "))
            if numero_inicial not in numeros_pendientes:
                print("Ese número ya fue conectado o no está disponible.")
        except ValueError:
            print("Debe ingresar un número válido.")
    
    return numero_inicial

def mover_direccion(movimientos_validos):
    print(f"Movimientos posibles: {', '.join(movimientos_validos)}")
    direccion = input("Ingrese la dirección de movimiento: ").strip().lower()

    while direccion not in movimientos_validos:
        print("Dirección inválida.")
        print(f"Movimientos posibles: {', '.join(movimientos_validos)}")
        direccion = input("Ingrese la dirección de movimiento: ").strip().lower()

    return direccion 

def verificar_movimientos_posibles(tablero, posicion_actual, posicion_anterior, numero_inicial):
    direcciones = {
        "arriba": (-1, 0),
        "abajo": (1, 0),
        "izquierda": (0, -1),
        "derecha": (0, 1)
    }

    movimientos_validos = []
    filas = len(tablero)
    columnas = len(tablero[0])
    fila_actual, col_actual = posicion_actual

    for direccion, desplazamiento in direcciones.items():
        nueva_fila = fila_actual + desplazamiento[0]
        nueva_col = col_actual + desplazamiento[1]

        if 0 <= nueva_fila < filas and 0 <= nueva_col < columnas and (tablero[nueva_fila][nueva_col] == 0 or tablero[nueva_fila][nueva_col] == numero_inicial):
            nueva_pos = (nueva_fila, nueva_col)

            if posicion_anterior is None or nueva_pos != posicion_anterior:
                movimientos_validos.append(direccion)

    return movimientos_validos


def validar_llegada(posicion_actual, puntos, numero_inicial):
    if posicion_actual in puntos[numero_inicial] and posicion_actual != puntos[numero_inicial][0]:
        print("¡Conexión completada para el número", numero_inicial, "!")
        return True
    return False

def validar_finalizacion(tablero):
    for fila in tablero:
        if 0 in fila:
            return False
    return True

def jugar():
    tablero, puntos = initialize()
    numeros_pendientes = list(puntos.keys())

    while numeros_pendientes:
        printTablero(tablero)
        numero_inicial = seleccionar_numero_inicial(numeros_pendientes)
        posicion_actual = puntos[numero_inicial][0]
        posicion_anterior = None

        while True:
            movimientos_validos = verificar_movimientos_posibles(tablero, posicion_actual, posicion_anterior, numero_inicial)

            if not movimientos_validos:
                print("No hay movimientos válidos. Termina este intento.")
                break
            printTablero(tablero)
            direccion = mover_direccion(movimientos_validos)

            if direccion == "arriba":
                nueva_pos = (posicion_actual[0] - 1, posicion_actual[1])
            elif direccion == "abajo":
                nueva_pos = (posicion_actual[0] + 1, posicion_actual[1])
            elif direccion == "izquierda":
                nueva_pos = (posicion_actual[0], posicion_actual[1] - 1)
            elif direccion == "derecha":
                nueva_pos = (posicion_actual[0], posicion_actual[1] + 1)

            tablero[nueva_pos[0]][nueva_pos[1]] = numero_inicial

            if validar_llegada(nueva_pos, puntos, numero_inicial):
                numeros_pendientes.remove(numero_inicial)
                break

            posicion_anterior = posicion_actual
            posicion_actual = nueva_pos

    print("¡Felicidades! Has completado todos los caminos.")

if __name__ == "__main__":
    jugar()