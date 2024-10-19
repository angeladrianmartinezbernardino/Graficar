import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

# Algoritmo de CastleJau para calcular la curva de Bézier.
def CastleJau(Puntos, t):
    while len(Puntos) > 1:
        Nuevos_puntos = []
        for i in range(len(Puntos) - 1):
            Nuevo_punto = (1 - t) * np.array(Puntos[i]) + t * np.array(Puntos[i + 1])
            Nuevos_puntos.append(Nuevo_punto)
        Puntos = Nuevos_puntos
    return Puntos[0]

# Función para dibujar la curva de Bézier con n puntos de control.
def Dinujar_curva_Bezier(Puntos, Numero_segmentos=100):
    glBegin(GL_LINE_STRIP)
    for i in range(Numero_segmentos + 1):
        t = i / Numero_segmentos
        Punto_Bezier = CastleJau(Puntos, t)
        glVertex2f(Punto_Bezier[0], Punto_Bezier[1])
    glEnd()

# Inicialización de la ventana y manejo de eventos.
def main():
    pygame.init()
    Pantalla = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Curva de Bézier con CastleJau")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    Puntos = []
    running = True
    while running:
        for Evento in pygame.event.get():
            if Evento.type == QUIT:
                running = False
            elif Evento.type == MOUSEBUTTONDOWN:
                if Evento.button == 1:  # Click izquierdo para agregar puntos de control.
                    x, y = Evento.pos
                    Puntos.append((x, y))
                elif Evento.button == 3:  # Click derecho para limpiar los puntos.
                    Puntos = []
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Dibujar puntos de control.
        glPointSize(5)
        glBegin(GL_POINTS)
        for point in Puntos:
            glVertex2f(point[0], point[1])
        glEnd()
        # Dibujar la curva de Bézier.
        if len(Puntos) >= 2:
            Dinujar_curva_Bezier(Puntos)
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()

if __name__ == "__main__":
    main()
