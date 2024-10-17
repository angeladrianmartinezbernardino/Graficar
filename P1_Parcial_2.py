import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# Definición de las Figuras del tangram
def dibujar_figuras():
    # Figura 1 - Triángulo grande naranja.
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0.65, 0)  # Color naranja.
    glVertex2f(0, 0)
    glVertex2f(-1, 1)
    glVertex2f(-1, -1)
    glEnd()
    # Figura 2 - Triángulo grande verde.
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0.5, 0)  # Color verde.
    glVertex2f(0, 0)
    glVertex2f(-1, 1)
    glVertex2f(1, 1)
    glEnd()
    # Figura 3 - Triángulo mediano rojo.
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)  # Color rojo.
    glVertex2f(1, -1)
    glVertex2f(1, 0)
    glVertex2f(0, -1)
    glEnd()
    # Figura 4 - Triángulo pequeño rosa.
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0.75, 0.8)  # Color rosa.
    glVertex2f(0, 0)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glEnd()
    # Figura 5 - Triángulo pequeño morado.
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0, 0.5)  # Color morado.
    glVertex2f(0.5, 0.5)
    glVertex2f(1, 1)
    glVertex2f(1, 0)
    glEnd()
    # Figura 6 - Cuadrado amarillo.
    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)  # Color amarillo.
    glVertex2f(0, 0)
    glVertex2f(0.5, 0.5)
    glVertex2f(1, 0)
    glVertex2f(0.5, -0.5)
    glEnd()
    # Figura 7 - Paralelogramo azul.
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)  # Color azul.
    glVertex2f(-1, -1)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(0, -1)
    glEnd()


def main():
    pygame.init()
    display = (1200, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        dibujar_figuras()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
