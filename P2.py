import pygame
import numpy as np
import time

# Inicializar pygame.
pygame.init()

# Definir colores.
Negro = (0, 0, 0)
Blanco = (255, 255, 255)
Rojo = (255, 0, 0)
Azul = (0, 0, 255)

# Establecer el tamaño de la ventana.
Tamaño_ventana = (300, 300)
Pantalla = pygame.display.set_mode(Tamaño_ventana)
pygame.display.set_caption("Juego del gato")

# Definir el tamaño de las celdas y el tablero.
Tamaño_celda = 100
Tablero = np.zeros((3, 3))


# Función para dibujar la cuadrícula.
def Dibujar_cuadricula():
    for x in range(1, 3):
        pygame.draw.line(Pantalla, Negro, (x * Tamaño_celda, 0), (x * Tamaño_celda, Tamaño_ventana[1]), 2)
    for y in range(1, 3):
        pygame.draw.line(Pantalla, Negro, (0, y * Tamaño_celda), (Tamaño_ventana[0], y * Tamaño_celda), 2)


# Función para dibujar la "x" y la "o".
def Dibujar_movimientos():
    for Fila in range(3):
        for Columna in range(3):
            if Tablero[Fila][Columna] == 1:
                pygame.draw.line(Pantalla, Rojo, (Columna * Tamaño_celda + 25, Fila * Tamaño_celda + 25),
                                 (Columna * Tamaño_celda + 75, Fila * Tamaño_celda + 75), 2)
                pygame.draw.line(Pantalla, Rojo, (Columna * Tamaño_celda + 75, Fila * Tamaño_celda + 25),
                                 (Columna * Tamaño_celda + 25, Fila * Tamaño_celda + 75), 2)
            elif Tablero[Fila][Columna] == 2:
                pygame.draw.circle(Pantalla, Azul, (Columna * Tamaño_celda + 50, Fila * Tamaño_celda + 50), 37, 2)


# Función para manejar los movimientos.
def Hacer_movimiento(Posicion, Jugador):
    if Posicion == 1:
        Fila, Columa = 2, 0
    elif Posicion == 2:
        Fila, Columa = 2, 1
    elif Posicion == 3:
        Fila, Columa = 2, 2
    elif Posicion == 4:
        Fila, Columa = 1, 0
    elif Posicion == 5:
        Fila, Columa = 1, 1
    elif Posicion == 6:
        Fila, Columa = 1, 2
    elif Posicion == 7:
        Fila, Columa = 0, 0
    elif Posicion == 8:
        Fila, Columa = 0, 1
    elif Posicion == 9:
        Fila, Columa = 0, 2

    if Tablero[Fila][Columa] == 0:
        Tablero[Fila][Columa] = Jugador


# Función para verificar el estado del juego.
def Verificar_ganador():
    # Verificar filas.
    for Fila in range(3):
        if Tablero[Fila][0] == Tablero[Fila][1] == Tablero[Fila][2] != 0:
            return Tablero[Fila][0]
    # Verificar columnas.
    for Columna in range(3):
        if Tablero[0][Columna] == Tablero[1][Columna] == Tablero[2][Columna] != 0:
            return Tablero[0][Columna]
    # Verificar diagonales.
    if Tablero[0][0] == Tablero[1][1] == Tablero[2][2] != 0:
        return Tablero[0][0]
    if Tablero[0][2] == Tablero[1][1] == Tablero[2][0] != 0:
        return Tablero[0][2]
    return 0


def Mover_con_raton(Fila, Columna, Jugador):
    Tablero[Fila][Columna] = Jugador
    pass


# Bucle principal del juego.
Ejecucion = True
Jugador_actual = 1

while Ejecucion:
    for Evento in pygame.event.get():
        if Evento.type == pygame.QUIT:
            Ejecucion = False
        if Evento.type == pygame.MOUSEBUTTONDOWN:
            Raton_x, Raton_y = pygame.mouse.get_pos()  # Obtener la posición del clic.

            Fila_clickeada = int(Raton_y // Tamaño_celda)
            Columna_clickeada = int(Raton_x // Tamaño_celda)

            # Convertir la fila y columna clickeada a la posición en el tablero.
            if Tablero[Fila_clickeada][Columna_clickeada] == 0:  # Verificar si la celda está vacía.
                Mover_con_raton(Fila_clickeada, Columna_clickeada, Jugador_actual)
                Jugador_actual = 1 if Jugador_actual == 2 else 2

    # Fondo de pantalla, dibujar la cuadrícula y movimientos, etcétera.
    Pantalla.fill(Blanco)
    Dibujar_cuadricula()
    Dibujar_movimientos()

    # Verificar si hay ganador.
    Ganador = Verificar_ganador()
    if Ganador:
        # Después de detectar un ganador, pero antes del reinicio del tablero.
        Fuente = pygame.font.Font(None, 36)  # None usa la fuente predeterminada, 36 es el tamaño del texto.
        Texto = Fuente.render(f'Jugador {Ganador} gana!', True, Negro)
        Texto_recto = Texto.get_rect(center=(Tamaño_ventana[0] / 2, Tamaño_ventana[1] / 2))
        Pantalla.fill(Blanco)  # Opcional, dependiendo de cómo quieras que se vea el mensaje.
        Pantalla.blit(Texto, Texto_recto)
        pygame.display.flip()
        time.sleep(5)  # Muestra el mensaje durante 5 segundos antes de reiniciar.
        Tablero = np.zeros((3, 3))  # Reiniciar el tablero.

    # Cambiar jugador.
    Jugador_actual = 1 if Jugador_actual == 2 else 2

    # Actualizar la pantalla.
    pygame.display.flip()

# Terminar pygame.
pygame.quit()
