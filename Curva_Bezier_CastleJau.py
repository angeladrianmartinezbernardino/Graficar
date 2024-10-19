import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# Algoritmo de CastleJau
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


# Función para dibujar la curva de Bézier
def draw_bezier_curve(points):
    if len(points) < 2:
        return
    glColor3f(1.0, 0.0, 0.0)  # Color rojo para la curva
    glBegin(GL_LINE_STRIP)
    for t in range(101):
        t /= 100.0
        p = CastleJau(points, t)
        if p:
            glVertex2f(p[0], p[1])
    glEnd()


# Función para dibujar los puntos de control
def draw_control_points(points):
    glColor3f(0.0, 1.0, 0.0)  # Color verde para los puntos
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Curva de Bézier con PyOpenGL")

    gluOrtho2D(0, 800, 0, 600)  # Configuración del espacio de coordenadas
    control_points = []  # Lista para almacenar los puntos de control

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo para añadir puntos de control
                    x, y = pygame.mouse.get_pos()
                    control_points.append((x, 600 - y))  # Ajuste de coordenadas para PyOpenGL
                elif event.button == 3:  # Botón derecho para reiniciar los puntos de control
                    control_points.clear()

        glClear(GL_COLOR_BUFFER_BIT)

        # Dibuja los puntos de control
        draw_control_points(control_points)

        # Dibuja la curva de Bézier si hay al menos dos puntos de control
        if len(control_points) >= 2:
            draw_bezier_curve(control_points)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
