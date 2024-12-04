import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import radians, sin, cos

# Definimos los vértices y las caras del cubo.
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1],
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Función para dibujar un cubo.
def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Convertir cuaternión a matriz de rotación.
def quaternion_to_matrix(q):
    w, x, y, z = q
    return [
        [1 - 2 * y ** 2 - 2 * z ** 2, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w, 0],
        [2 * x * y + 2 * z * w, 1 - 2 * x ** 2 - 2 * z ** 2, 2 * y * z - 2 * x * w, 0],
        [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x ** 2 - 2 * y ** 2, 0],
        [0, 0, 0, 1]
    ]

# Generar un cuaternión de rotación.
def create_quaternion(axis, angle_degrees):
    angle_radians = radians(angle_degrees)
    half_angle = angle_radians / 2
    w = cos(half_angle)
    x, y, z = [a * sin(half_angle) for a in axis]
    return w, x, y, z

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    axis = [0, 1, 0]  # Eje Y.
    angle = 0  # Ángulo inicial.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Incrementar ángulo.
        angle += 1
        if angle >= 360:
            angle = 0

        # Crear cuaternión y obtener matriz de rotación.
        q = create_quaternion(axis, angle)
        rotation_matrix = quaternion_to_matrix(q)

        # Limpiar pantalla y aplicar transformación.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glMultMatrixf(np.array(rotation_matrix, dtype=np.float32))  # Multiplicar matriz.
        draw_cube()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
