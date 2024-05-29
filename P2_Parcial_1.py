import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time

# De Ángel Adrián Martínez Bernardino y Luis Carlos Prieto Juárez.

# Inicializar pygame y OpenGL.
pygame.init()
display = (300, 300)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Configurar la vista ortográfica.
gluOrtho2D(0, 300, 300, 0)

# Definir colores en formato RGB OpenGL.
Negro = (0, 0, 0)
Blanco = (1, 1, 1)
Rojo = (1, 0, 0)
Azul = (0, 0, 1)

# Inicializar el tablero.
Tablero = np.zeros((3, 3))

def dibujar_cuadricula():
    glLineWidth(2)
    glColor3fv(Negro)
    glBegin(GL_LINES)
    # Dibujar las líneas verticales de la cuadrícula.
    for x in range(1, 3):
        glVertex2f(x * 100, 0)
        glVertex2f(x * 100, 300)
    # Dibujar las líneas horizontales de la cuadrícula.
    for y in range(1, 3):
        glVertex2f(0, y * 100)
        glVertex2f(300, y * 100)
    glEnd()

def dibujar_movimientos():
    for Fila in range(3):
        for Columna in range(3):
            Centro_x = Columna * 100 + 50
            Centro_y = Fila * 100 + 50
            if Tablero[Fila][Columna] == 1:
                glLineWidth(2)
                glColor3fv(Rojo)
                glBegin(GL_LINES)
                glVertex2f(Centro_x - 25, Centro_y - 25)
                glVertex2f(Centro_x + 25, Centro_y + 25)
                glVertex2f(Centro_x + 25, Centro_y - 25)
                glVertex2f(Centro_x - 25, Centro_y + 25)
                glEnd()
            elif Tablero[Fila][Columna] == 2:
                glColor3fv(Azul)
                glBegin(GL_LINE_LOOP)
                for i in range(360):
                    rad = np.radians(i)
                    glVertex2f(np.cos(rad) * 37 + Centro_x, np.sin(rad) * 37 + Centro_y)
                glEnd()

def reiniciar_juego():
    global Tablero
    Tablero = np.zeros((3, 3))
    main()

def main():
    Ejecucion = True
    Jugador_actual = 1
    while Ejecucion:
        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                Ejecucion = False
            elif Evento.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                Columna = x // 100
                Fila = y // 100
                if Tablero[int(Fila)][int(Columna)] == 0:
                    Tablero[int(Fila)][int(Columna)] = Jugador_actual
                    Jugador_actual = 3 - Jugador_actual  # Alterna entre 1 y 2.
                    # Limpiar pantalla.
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                    glClearColor(1, 1, 1, 1)  # Fondo blanco.
                    # Dibujar la cuadrícula y los movimientos.
                    dibujar_cuadricula()
                    dibujar_movimientos()
                    pygame.display.flip()
                    Ganador = verificar_ganador()
                    if Ganador:
                        print(f'¡El jugador {Ganador} ha ganado!')
                        pygame.time.wait(2500)  # Espera breve para mostrar la última jugada.
                        pygame.display.flip()
                        time.sleep(5)
                        reiniciar_juego()
                    elif np.all(Tablero != 0):
                        print('¡Empate!')
                        pygame.time.wait(2500)  # Espera breve para mostrar la última jugada.
                        pygame.display.flip()
                        time.sleep(5)
                        reiniciar_juego()

        # Limpiar pantalla.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)  # Fondo blanco.
        # Dibujar la cuadrícula y los movimientos.
        dibujar_cuadricula()
        dibujar_movimientos()
        pygame.display.flip()
        pygame.time.wait(10)

def verificar_ganador():
    # Verifica filas, columnas y diagonales para encontrar un ganador.
    for i in range(3):
        if Tablero[i][0] == Tablero[i][1] == Tablero[i][2] != 0:
            return Tablero[i][0]
        if Tablero[0][i] == Tablero[1][i] == Tablero[2][i] != 0:
            return Tablero[0][i]
    if Tablero[0][0] == Tablero[1][1] == Tablero[2][2] != 0 or Tablero[0][2] == Tablero[1][1] == Tablero[2][0] != 0:
        return Tablero[1][1]
    return None

if __name__ == "__main__":
    main()
