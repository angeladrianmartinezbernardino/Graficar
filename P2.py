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
board = np.zeros((3, 3))


# Función para dibujar la cuadrícula.
def draw_grid():
    for x in range(1, 3):
        pygame.draw.line(Pantalla, Negro, (x * Tamaño_celda, 0), (x * Tamaño_celda, Tamaño_ventana[1]), 2)
    for y in range(1, 3):
        pygame.draw.line(Pantalla, Negro, (0, y * Tamaño_celda), (Tamaño_ventana[0], y * Tamaño_celda), 2)


# Función para dibujar la "x" y la "o".
def draw_moves():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                pygame.draw.line(Pantalla, Rojo, (col * Tamaño_celda + 25, row * Tamaño_celda + 25),
                                 (col * Tamaño_celda + 75, row * Tamaño_celda + 75), 2)
                pygame.draw.line(Pantalla, Rojo, (col * Tamaño_celda + 75, row * Tamaño_celda + 25),
                                 (col * Tamaño_celda + 25, row * Tamaño_celda + 75), 2)
            elif board[row][col] == 2:
                pygame.draw.circle(Pantalla, Azul, (col * Tamaño_celda + 50, row * Tamaño_celda + 50), 37, 2)


# Función para manejar los movimientos.
def make_move(position, player):
    if position == 1:
        row, col = 2, 0
    elif position == 2:
        row, col = 2, 1
    elif position == 3:
        row, col = 2, 2
    elif position == 4:
        row, col = 1, 0
    elif position == 5:
        row, col = 1, 1
    elif position == 6:
        row, col = 1, 2
    elif position == 7:
        row, col = 0, 0
    elif position == 8:
        row, col = 0, 1
    elif position == 9:
        row, col = 0, 2

    if board[row][col] == 0:
        board[row][col] = player


# Función para verificar el estado del juego.
def check_win():
    # Verificar filas.
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            return board[row][0]
    # Verificar columnas.
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return board[0][col]
    # Verificar diagonales.
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0


def make_move_based_on_mouse(row, col, player):
    board[row][col] = player
    pass


# Bucle principal del juego.
running = True
current_player = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()  # Obtener la posición del clic.

            clicked_row = int(mouseY // Tamaño_celda)
            clicked_col = int(mouseX // Tamaño_celda)

            # Convertir la fila y columna clickeada a la posición en el tablero.
            if board[clicked_row][clicked_col] == 0:  # Verificar si la celda está vacía
                make_move_based_on_mouse(clicked_row, clicked_col, current_player)
                current_player = 1 if current_player == 2 else 2

    # Fondo de pantalla, dibujar la cuadrícula y movimientos, etcétera.
    Pantalla.fill(Blanco)
    draw_grid()
    draw_moves()

    # Verificar si hay ganador.
    winner = check_win()
    if winner:
        # Después de detectar un ganador, pero antes del reinicio del tablero.
        font = pygame.font.Font(None, 36)  # None usa la fuente predeterminada, 36 es el tamaño del texto.
        text = font.render(f'Jugador {winner} gana!', True, Negro)
        text_rect = text.get_rect(center=(Tamaño_ventana[0] / 2, Tamaño_ventana[1] / 2))
        Pantalla.fill(Blanco)  # Opcional, dependiendo de cómo quieras que se vea el mensaje.
        Pantalla.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(5)  # Muestra el mensaje durante 5 segundos antes de reiniciar.
        board = np.zeros((3, 3))  # Reiniciar el tablero.

    # Cambiar jugador.
    current_player = 1 if current_player == 2 else 2

    # Actualizar la pantalla.
    pygame.display.flip()

# Terminar pygame.
pygame.quit()