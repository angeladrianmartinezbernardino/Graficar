import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Definición de vértices y aristas del cubo.
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
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]

def draw_cube():
    """Dibuja un cubo en pantalla usando vértices y aristas."""
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def quaternion_rotation(q, v):
    """Aplica la rotación definida por un cuaternión a un vector."""
    q_conj = q * np.array([1, -1, -1, -1])
    v_quat = np.array([0] + v)
    rotated_v = quaternion_multiply(quaternion_multiply(q, v_quat), q_conj)
    return rotated_v[1:]

def quaternion_multiply(q1, q2):
    """Multiplica dos cuaterniones."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Cuaternión inicial (sin rotación).
    quaternion = np.array([1, 0, 0, 0])

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Entrada para rotar el cubo.
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            # Rotar 5 grados en el eje Y.
            angle = np.radians(5)
            axis = np.array([0, 1, 0])
            delta_q = np.array([np.cos(angle / 2), *(np.sin(angle / 2) * axis)])
            quaternion = quaternion_multiply(delta_q, quaternion)

        if keys[K_RIGHT]:
            # Rotar -5 grados en el eje Y.
            angle = np.radians(-5)
            axis = np.array([0, 1, 0])
            delta_q = np.array([np.cos(angle / 2), *(np.sin(angle / 2) * axis)])
            quaternion = quaternion_multiply(delta_q, quaternion)

        if keys[K_UP]:
            # Rotar 5 grados en el eje X.
            angle = np.radians(5)
            axis = np.array([1, 0, 0])
            delta_q = np.array([np.cos(angle / 2), *(np.sin(angle / 2) * axis)])
            quaternion = quaternion_multiply(delta_q, quaternion)

        if keys[K_DOWN]:
            # Rotar -5 grados en el eje X.
            angle = np.radians(-5)
            axis = np.array([1, 0, 0])
            delta_q = np.array([np.cos(angle / 2), *(np.sin(angle / 2) * axis)])
            quaternion = quaternion_multiply(delta_q, quaternion)

        # Aplicar rotación del cuaternión.
        rotation_matrix = np.eye(4)
        rotation_matrix[:3, :3] = np.linalg.qr(np.array([
            quaternion_rotation(quaternion, [1, 0, 0]),
            quaternion_rotation(quaternion, [0, 1, 0]),
            quaternion_rotation(quaternion, [0, 0, 1])
        ]).T)[0]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glMultMatrixf(rotation_matrix.flatten())
        draw_cube()
        glPopMatrix()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
