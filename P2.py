import pygame
import numpy as np
import time

# Inicializar pygame.
pygame.init()

# Definir colores.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Establecer el tamaño de la ventana.
window_size = (300, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Juego del Gato")

# Definir el tamaño de las celdas y el tablero.
cell_size = 100
board = np.zeros((3, 3))


# Función para dibujar la cuadrícula.
def draw_grid():
    for x in range(1, 3):
        pygame.draw.line(screen, BLACK, (x * cell_size, 0), (x * cell_size, window_size[1]), 2)
    for y in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, y * cell_size), (window_size[0], y * cell_size), 2)


# Función para dibujar la "x" y la "o".
def draw_moves():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                pygame.draw.line(screen, RED, (col * cell_size + 25, row * cell_size + 25),
                                 (col * cell_size + 75, row * cell_size + 75), 2)
                pygame.draw.line(screen, RED, (col * cell_size + 75, row * cell_size + 25),
                                 (col * cell_size + 25, row * cell_size + 75), 2)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, BLUE, (col * cell_size + 50, row * cell_size + 50), 37, 2)


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

            clicked_row = int(mouseY // cell_size)
            clicked_col = int(mouseX // cell_size)

            # Convertir la fila y columna clickeada a la posición en el tablero.
            if board[clicked_row][clicked_col] == 0:  # Verificar si la celda está vacía
                make_move_based_on_mouse(clicked_row, clicked_col, current_player)
                current_player = 1 if current_player == 2 else 2

    # Fondo de pantalla, dibujar la cuadrícula y movimientos, etcétera.
    screen.fill(WHITE)
    draw_grid()
    draw_moves()

    # Verificar si hay ganador.
    winner = check_win()
    if winner:
        print(f"¡El jugador {winner} ganó!")
        time.sleep(5)
        board = np.zeros((3, 3))  # Reiniciar el tablero.

    # Cambiar jugador.
    current_player = 1 if current_player == 2 else 2

    # Actualizar la pantalla.
    pygame.display.flip()

# Terminar pygame.
pygame.quit()
