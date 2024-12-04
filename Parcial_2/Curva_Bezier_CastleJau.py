import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Algoritmo de CastleJau.
def CastleJau(input, t):
    i = 0
    s = []
    l = len(input)
    if (l == 0):
        return None
    if (l == 1):
        return input[0]
    if (t < 0.0 or t > 1.0):
        return None
    while (i < l):
        if ((i + 1) < l):
            x = (1.0 - t) * input[i][0] + t * input[i + 1][0]
            y = (1.0 - t) * input[i][1] + t * input[i + 1][1]
            s.append((x, y))
        i += 1
    if len(s) == 1:
        return s[0]
    return CastleJau(s, t)

# Función para dibujar la curva de Bézier.
def Dibujar_curva_Bezier(points):
    if len(points) < 2:
        return
    glColor3f(1.0, 0.0, 0.0)  # Color rojo para la curva.
    glBegin(GL_LINE_STRIP)
    for t in range(101):
        t /= 100.0
        p = CastleJau(points, t)
        if p:
            glVertex2f(p[0], p[1])
    glEnd()

# Función para dibujar los puntos de control.
def Dibujar_puntos_control(Puntos):
    glColor3f(0.0, 1.0, 0.0)  # Color verde para los puntos.
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in Puntos:
        glVertex2f(p[0], p[1])
    glEnd()

def main():
    pygame.init()
    Pantalla = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Curva de Bézier con OpenGL")
    gluOrtho2D(0, 800, 0, 600)  # Configuración del espacio de coordenadas.
    Puntos_control = []  # Lista para almacenar los puntos de control.
    Ejecucion = True
    while Ejecucion:
        for Evento in pygame.event.get():
            if Evento.type == QUIT:
                Ejecucion = False
            elif Evento.type == MOUSEBUTTONDOWN:
                if Evento.button == 1:  # Botón izquierdo para añadir puntos de control.
                    x, y = pygame.mouse.get_pos()
                    Puntos_control.append((x, 600 - y))  # Ajuste de coordenadas para PyOpenGL.
                elif Evento.button == 3:  # Botón derecho para reiniciar los puntos de control.
                    Puntos_control.clear()
        glClear(GL_COLOR_BUFFER_BIT)
        # Dibuja los puntos de control.
        Dibujar_puntos_control(Puntos_control)
        # Dibuja la curva de Bézier si hay al menos dos puntos de control.
        if len(Puntos_control) >= 2:
            Dibujar_curva_Bezier(Puntos_control)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
