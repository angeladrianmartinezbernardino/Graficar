import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Dimensiones de la ventana y del tablero
Ancho, Altura = 424, 254
Margen_X = 18
Margen_Y = 15
Tamaño_Casilla_Ancho = (Ancho - (2 * Margen_X)) / 10  # Ancho de las casillas
Tamaño_Casilla_Alto = (Altura - (2 * Margen_Y)) / 10  # Alto de las casillas
Tablero_Ancho = 10  # Número de casillas en el tablero
Tablero_Alto = 10

# Posición inicial del cubo
Posicion_cubo = [5, 5]  # Centro del tablero

# Función para inicializar PyOpenGL con ajuste a la ventana y perspectiva
def Vistas():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, Ancho, 0, Altura)  # Proyección ortográfica ajustada al tamaño de la ventana
    glMatrixMode(GL_MODELVIEW)

# Función para convertir las coordenadas 2D del tablero en coordenadas isométricas
def Isometrico(x, y):
    # Cálculo de las coordenadas isométricas
    X_isometrico = ((Tablero_Ancho - 1 - y) - (Tablero_Ancho - 1 - x)) * (Tamaño_Casilla_Ancho / 2)
    Y_isometrico = ((Tablero_Ancho - 1 - x) + (Tablero_Ancho - 1 - y)) * (Tamaño_Casilla_Alto / 2)
    # Ajustar con los márgenes
    X_final = X_isometrico + (Ancho / 2)
    Y_final = Y_isometrico + Margen_Y
    return X_final, Y_final

# Función para convertir las coordenadas 3D del tablero en coordenadas isométricas
def Isometrico3D(x, y, z):
    X_isometrico = (x - y) * (Tamaño_Casilla_Ancho / 2)
    Y_isometrico = (x + y) * (Tamaño_Casilla_Alto / 2) - z * Tamaño_Casilla_Alto
    # Ajustar con los márgenes
    X_final = X_isometrico + (Ancho / 2)
    Y_final = Y_isometrico + Margen_Y
    return X_final, Y_final

# Función para dibujar el tablero
def Dibujar_grid():
    for i in range(Tablero_Ancho):
        for j in range(Tablero_Alto):
            Dibujar_casilla(i, j)

# Función para dibujar una casilla en una posición (x, y) en la vista isométrica
def Dibujar_casilla(x, y):
    X_isometrico, Y_isometrico = Isometrico(x, y)
    half_width = Tamaño_Casilla_Ancho / 2
    half_height = Tamaño_Casilla_Alto / 2
    # Dibujo de la casilla (color de fondo azul claro)
    glColor3fv((0.70, 0.85, 0.90))  # Azul claro
    glBegin(GL_QUADS)
    glVertex3f(X_isometrico, Y_isometrico, 0.0)
    glVertex3f(X_isometrico + half_width, Y_isometrico + half_height, 0.0)
    glVertex3f(X_isometrico, Y_isometrico + Tamaño_Casilla_Alto, 0.0)
    glVertex3f(X_isometrico - half_width, Y_isometrico + half_height, 0.0)
    glEnd()
    # Dibujo de las líneas de la casilla (color de las líneas negras)
    glColor3fv((0.0, 0.0, 0.0))  # Líneas negras
    glBegin(GL_LINE_LOOP)
    glVertex3f(X_isometrico, Y_isometrico, 0.0)
    glVertex3f(X_isometrico + half_width, Y_isometrico + half_height, 0.0)
    glVertex3f(X_isometrico, Y_isometrico + Tamaño_Casilla_Alto, 0.0)
    glVertex3f(X_isometrico - half_width, Y_isometrico + half_height, 0.0)
    glEnd()

# Función para dibujar un cubo en una posición (x, y) en la vista isométrica
def Dibujar_cubo(x, y):
    # Definir los vértices del cubo en coordenadas de grilla
    h = 1  # Altura del cubo en unidades de grilla
    Vertices = [
        [x, y, 0],         # 0
        [x + 1, y, 0],     # 1
        [x + 1, y + 1, 0], # 2
        [x, y + 1, 0],     # 3
        [x, y, h],         # 4
        [x + 1, y, h],     # 5
        [x + 1, y + 1, h], # 6
        [x, y + 1, h]      # 7
    ]

    # Convertir los vértices a coordenadas de pantalla
    Screen_Vertices = []
    for vx, vy, vz in Vertices:
        sx, sy = Isometrico3D(vx, vy, vz)
        Screen_Vertices.append((sx, sy))

    # Definir las caras del cubo
    Faces = [
        [0, 1, 5, 4],  # Cara frontal
        [1, 2, 6, 5],  # Cara derecha
        [4, 5, 6, 7],  # Cara superior
        # Puedes agregar más caras si es necesario
    ]

    # Dibujar las caras del cubo
    glColor3fv((1.0, 0.0, 0.0))  # Rojo para las caras del cubo
    glBegin(GL_QUADS)
    for face in Faces:
        for vertex in face:
            sx, sy = Screen_Vertices[vertex]
            glVertex3f(sx, sy, 0.0)
    glEnd()

    # Dibujar las aristas del cubo
    Edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    glColor3fv((0.0, 0.0, 0.0))  # Negro para las aristas
    glBegin(GL_LINES)
    for edge in Edges:
        for vertex in edge:
            sx, sy = Screen_Vertices[vertex]
            glVertex3f(sx, sy, 0.0)
    glEnd()

# Función para mover el cubo
def Mover_cubo(Tecla, Posicion_cubo):
    if Tecla == K_LEFT and Posicion_cubo[0] > 0:
        Posicion_cubo[0] -= 1
    if Tecla == K_RIGHT and Posicion_cubo[0] < Tablero_Ancho - 1:
        Posicion_cubo[0] += 1
    if Tecla == K_UP and Posicion_cubo[1] > 0:
        Posicion_cubo[1] -= 1
    if Tecla == K_DOWN and Posicion_cubo[1] < Tablero_Alto - 1:
        Posicion_cubo[1] += 1

# Función principal del programa
def Main():
    pygame.init()
    pygame.display.set_mode((Ancho, Altura), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Tablero isométrico con cubo movible')
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Cambiar el fondo a blanco
    Vistas()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                Mover_cubo(event.key, Posicion_cubo)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Dibujar_grid()
        Dibujar_cubo(Posicion_cubo[0], Posicion_cubo[1])
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    Main()
