import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


class Figura:
    def __init__(self, vertices, color):

        self.vertices = vertices
    self.color = color
    self.direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -
    1)])  # Dirección aleatoria para empezar

    def dibujar(self):

        glBegin(GL_POLYGON)
    glColor3fv(self.color)
    for vertex in self.vertices:
        glVertex2fv(vertex)
    glEnd()

    def mover(self, bounds):

    # Movimiento de la figura
    for i in range(len(self.vertices)):
        self.vertices[i] = (self.vertices[i][0] + self.direction[0],
                            self.vertices[i][1] + self.direction[1])
    # Revisar los límites de la pantalla para rebote
    for i in range(len(self.vertices)):
        if self.vertices[i][0] >= bounds[0] or self.vertices[i][0] <=


-bounds[0]:
self.direction = (-self.direction[0], self.direction[1])
if self.vertices[i][1] >= bounds[1] or self.vertices[i][1] <=
-bounds[1]:
self.direction = (self.direction[0], -self.direction[1])


def dibujar_figuras(figuras):
    for figura in figuras:
        figura.dibujar()


def main():
    pygame.init()
    display = (1200, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -5)
    figuras = [
        Figura([(0, 0), (-1, 1), (-1, -1)], (1, 0.65, 0)),  # Triángulo
        grande naranja
        Figura([(0, 0), (-1, 1), (1, 1)], (0, 0.5, 0)),  # Triángulo
        grande verde
        Figura([(1, -1), (1, 0), (0, -1)], (1, 0, 0)),  # Triángulo
        mediano rojo
        Figura([(0, 0), (-0.5, -0.5), (0.5, -0.5)], (1, 0.75, 0.8)),  #
        Triángulo pequeño rosa
        Figura([(0.5, 0.5), (1, 1), (1, 0)], (0.5, 0, 0.5)),  # Triángulo
        pequeño morado
        Figura([(0, 0), (0.5, 0.5), (1, 0), (0.5, -0.5)], (1, 1, 0)),  #
        Cuadrado amarillo
        Figura([(-1, -1), (-0.5, -0.5), (0.5, -0.5), (0, -1)], (0, 0, 1))
        # Paralelogramo azul
    ]
    bounds = (display[0] // 2 - 1, display[1] // 2 - 1)  # Límites de la


pantalla
while True:
    for event in pygame.event.get():
    if event.type == pygame.QUIT:
    pygame.quit()
quit()
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
# Movimiento de las figuras
for figura in figuras:
    figura.mover(bounds)
dibujar_figuras(figuras)
pygame.display.flip()
pygame.time.wait(3600)
if __name__ == "__main__":
    main()
