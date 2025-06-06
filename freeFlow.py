def initialize():
    """
    Inicializa el tablero y los puntos a partir de un archivo de entrada.

    Retorna:
    - tablero: matriz con los números colocados en sus posiciones iniciales
    - puntos: diccionario que agrupa las coordenadas de cada número
    """  

    lineas = []
    with open("entradas\entrada.txt", "r") as archivo:
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

        # Agregar la posición al diccionario de puntos
        if numero not in puntos:
            puntos[numero] = [(fila, columna)]
        else:
            puntos[numero].append((fila, columna))

    return tablero, puntos


def printTablero(tablero, posicion_actual=None):
    """
    Imprime el estado actual del tablero, resaltando la posición del jugador si se proporciona.
    """
    RESET = "\033[0m"
    HIGHLIGHT = "\033[1;37;41m"  # texto blanco brillante, fondo rojo

    print("_______________________")
    for i, fila in enumerate(tablero):
        print("|", end=" ")
        for j, valor in enumerate(fila):
            if (i, j) == posicion_actual:
                print(f"{HIGHLIGHT}{valor}{RESET}", end="  ")
            else:
                print(f"{valor}", end="  ")
        print("|")
    print("_______________________")
def seleccionar_numero_inicial(numeros_pendientes):
    """
    Solicita al jugador que seleccione un número válido aún pendiente de conexión.
    """

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
    """
    Solicita al jugador una dirección de movimiento válida entre las disponibles.
    
    Retorna:
    - La dirección elegida por el jugador.
    """
    movimientos_validos_con_reinicio = movimientos_validos + ["reiniciar"]
    
    print(f"Movimientos posibles: {', '.join(movimientos_validos)} (o escribe 'reiniciar')")
    direccion = input("Ingrese la dirección de movimiento: ").strip().lower()

    # Validar que la dirección esté entre las opciones disponibles
    while direccion not in movimientos_validos_con_reinicio:
        print("Dirección inválida.")
        print(f"Movimientos posibles: {', '.join(movimientos_validos)} (o escribe 'reiniciar')")
        direccion = input("Ingrese la dirección de movimiento: ").strip().lower()

    return direccion 

def verificar_movimientos_posibles(tablero, posicion_actual, posicion_anterior, numero_inicial):
    """
    Retorna una lista de direcciones válidas desde la posición actual,
    evitando retroceder a la posición anterior y respetando las reglas del juego.
    """
    # Diccionario de direcciones posibles con su desplazamiento
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

    # Evaluar cada dirección posible
    for direccion, desplazamiento in direcciones.items():
        nueva_fila = fila_actual + desplazamiento[0]
        nueva_col = col_actual + desplazamiento[1]

        # Verificar que la posicion nueva este dentro del tablero y permitir moverse a celdas vacías o con el mismo número
        if 0 <= nueva_fila < filas and 0 <= nueva_col < columnas and (tablero[nueva_fila][nueva_col] == 0 or tablero[nueva_fila][nueva_col] == numero_inicial):
            nueva_pos = (nueva_fila, nueva_col)

            # Evitar retroceder a la posición anterior
            if posicion_anterior is None or nueva_pos != posicion_anterior:
                movimientos_validos.append(direccion)

    return movimientos_validos


def validar_llegada(posicion_actual, puntos, numero_inicial):
    """
    Verifica si el jugador ha llegado a la segunda posición correspondiente al número seleccionado.

    Retorna:
    - True si la posición actual es la segunda coordenada del número.
    - False en caso contrario.
    """

    if posicion_actual in puntos[numero_inicial] and posicion_actual != puntos[numero_inicial][0]:
        print("¡Conexión completada para el número", numero_inicial, "!")
        return True
    return False

def validar_finalizacion(tablero):
    """
    Verifica si el tablero está completamente lleno, sin celdas vacías.

    Retorna:
    - True si no quedan ceros en el tablero.
    - False si aún hay al menos una celda vacía.
    """
        
    for fila in tablero:
        if 0 in fila:
            return False
    return True

def jugar():
    """
    Controla el flujo principal del juego.
    Permite seleccionar un número, moverse paso a paso y verificar la finalización del tablero.
    """
    # Inicializar el tablero y obtener las posiciones de los pares
    tablero, puntos = initialize()
    numeros_pendientes = list(puntos.keys())
    trazo_actual = []

    # Ciclo principal: mientras haya números por conectar
    while numeros_pendientes:
        printTablero(tablero, posicion_actual=None)
        numero_inicial = seleccionar_numero_inicial(numeros_pendientes)
        posicion_actual = puntos[numero_inicial][0]
        posicion_anterior = None

        # Ciclo de movimientos para el número seleccionado
        while True:
            # Obtener las direcciones posibles desde la posición actual
            movimientos_validos = verificar_movimientos_posibles(tablero, posicion_actual, posicion_anterior, numero_inicial)

            if not movimientos_validos:
                print("No hay movimientos válidos. Termina este intento.")
                break
            printTablero(tablero, posicion_actual)
            direccion = mover_direccion(movimientos_validos)
            
            if direccion == "reiniciar":
                for fila, col in trazo_actual:
                    if (fila, col) not in puntos[numero_inicial] and tablero[fila][col] == numero_inicial:
                        tablero[fila][col] = 0
                print("Se reinició el trazo para el número", numero_inicial)
                posicion_actual = puntos[numero_inicial][0]
                posicion_anterior = None
                trazo_actual = []
                continue

            # Calcular la nueva posición según la dirección elegida
            if direccion == "arriba":
                nueva_pos = (posicion_actual[0] - 1, posicion_actual[1])
            elif direccion == "abajo":
                nueva_pos = (posicion_actual[0] + 1, posicion_actual[1])
            elif direccion == "izquierda":
                nueva_pos = (posicion_actual[0], posicion_actual[1] - 1)
            elif direccion == "derecha":
                nueva_pos = (posicion_actual[0], posicion_actual[1] + 1)

            # Marcar el número en el tablero
            tablero[nueva_pos[0]][nueva_pos[1]] = numero_inicial
            trazo_actual.append(nueva_pos) 

            # Verificar si se llegó a la segunda posición del número
            if validar_llegada(nueva_pos, puntos, numero_inicial):
                numeros_pendientes.remove(numero_inicial)
                break
            
            # Actualizar posiciones para el siguiente paso
            posicion_anterior = posicion_actual
            posicion_actual = nueva_pos

    # Evaluar si realmente se completó todo el tablero
    if not validar_finalizacion(tablero):
        print("Pese a que conectaste todos los numeros posibles, no pudiste completar todos los caminos. Intenta de nuevo.")

    print("¡Felicidades! Has completado todos los caminos.")

if __name__ == "__main__":
    jugar()