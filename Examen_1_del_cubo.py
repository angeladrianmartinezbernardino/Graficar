import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# De Ángel Adrián Martínez Bernardino.
# Examen del Parcial 1.

# Definir la configuración inicial de la ventana.
Ancho, Altura = 560, 560

# Tamaño del tablero.
Tamano_tablero = 10

# Posición inicial del cubo.
Posicion_cubo = [5, 5]  # Centro del tablero.

# Función para inicializar PyOpenGL.
def Vistas():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(80, (Ancho / Altura), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(15, 15, 15, -5, 0, -5, 0, 1, 0) # Ajusta la vista para centrar el tablero.

# Función para dibujar el tablero isométrico.
def Dibujar_tablero_isometrico():
    glBegin(GL_LINES)
    # Dibuja las líneas horizontales.
    for i in range(Tamano_tablero + 1):
        if i == 0 or i == Tamano_tablero:
            glColor3fv((1, 1, 1))  # Líneas blancas.
        else:
            glColor3fv((0.7, 0.7, 0.7))  # Líneas grises.
        glVertex3fv((i, 0, 0))
        glVertex3fv((i, 0, Tamano_tablero))
    # Dibuja las líneas verticales.
    for j in range(Tamano_tablero + 1):
        if j == 0 or j == Tamano_tablero:
            glColor3fv((1, 1, 1))  # Líneas blancas.
        else:
            glColor3fv((0.7, 0.7, 0.7))  # Líneas grises.
        glVertex3fv((0, 0, j))
        glVertex3fv((Tamano_tablero, 0, j))
    glEnd()

# Función para dibujar el cubo.
def Dibujar_cubo(x, y):
    # Dibujar cubo sólido rojo
    glColor3fv((1, 0, 0))  # Rojo.
    glBegin(GL_QUADS)
    Vertices = [
        [x, 0, y],
        [x + 1, 0, y],
        [x + 1, 1, y],
        [x, 1, y],
        [x, 0, y + 1],
        [x + 1, 0, y + 1],
        [x + 1, 1, y + 1],
        [x, 1, y + 1]
    ]
    Caras = [
        [0, 1, 2, 3],  # Cara inferior.
        [4, 5, 6, 7],  # Cara superior.
        [0, 1, 5, 4],  # Cara frontal.
        [2, 3, 7, 6],  # Cara trasera.
        [1, 2, 6, 5],  # Cara derecha.
        [0, 3, 7, 4]  # Cara izquierda.
    ]
    for Cara in Caras:
        for Vertice in Cara:
            glVertex3fv(Vertices[Vertice])
    glEnd()
    # Dibujar contorno del cubo en blanco.
    glColor3fv((1, 1, 1))  # Blanco para el contorno.
    glBegin(GL_LINE_LOOP)  # Contorno de la cara inferior.
    for v in [0, 1, 2, 3]:
        glVertex3fv(Vertices[v])
    glEnd()
    glBegin(GL_LINE_LOOP)  # Contorno de la cara superior.
    for v in [4, 5, 6, 7]:
        glVertex3fv(Vertices[v])
    glEnd()
    glBegin(GL_LINES)  # Contorno de las aristas verticales.
    for v1, v2 in [(0, 4), (1, 5), (2, 6), (3, 7)]:
        glVertex3fv(Vertices[v1])
        glVertex3fv(Vertices[v2])
    glEnd()

# Función para mover el cubo.
def Mover_cubo(Tecla, Posicion_cubo):
    if Tecla == K_LEFT and Posicion_cubo[0] > 0:
        Posicion_cubo[0] -= 1
    if Tecla == K_RIGHT and Posicion_cubo[0] < Tamano_tablero - 1:
        Posicion_cubo[0] += 1
    if Tecla == K_UP and Posicion_cubo[1] > 0:
        Posicion_cubo[1] -= 1
    if Tecla == K_DOWN and Posicion_cubo[1] < Tamano_tablero - 1:
        Posicion_cubo[1] += 1

# Función principal.
def Main():
    pygame.init()
    pygame.display.set_mode((Ancho, Altura), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Tablero isométrico con cubo movible')
    Vistas()
    while True:
        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                pygame.quit()
                return
            if Evento.type == pygame.KEYDOWN:
                Mover_cubo(Evento.key, Posicion_cubo)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Dibujar_tablero_isometrico()
        Dibujar_cubo(Posicion_cubo[0], Posicion_cubo[1])
        pygame.display.flip()
        pygame.time.wait(100)

if __name__ == '__main__':
    Main()
