import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# De Ángel Adrián Martínez Bernardino y Luis Carlos Prieto Juárez.
# Inicializa pygame y crea una ventana.
pygame.init()
Pantalla = (800, 600)
pygame.display.set_mode(Pantalla, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Función seno")
# Establece el punto de vista de la cámara.
gluPerspective(45, (Pantalla[0] / Pantalla[1]), 0.1, 50.0)
# Mueve la cámara hacia atrás para que podamos ver el objeto (la función seno).
glTranslatef(0.0, 0.0, -5)


# Función para dibujar los ejes x e y.
def Dibujar_ejes():
    glLineWidth(2.0)  # Hace los ejes un poco más gruesos.
    glBegin(GL_LINES)
    # Eje x.
    glColor3f(0.0, 0.0, 0.0)  # Negro.
    glVertex3fv((-5, 0, 0))
    glVertex3fv((5, 0, 0))
    # Eje y.
    glVertex3fv((0, -5, 0))
    glVertex3fv((0, 5, 0))
    glEnd()


# Función para dibujar la función seno.
def Dibujar_onda_sinusoidal():
    glColor3f(1.0, 0.0, 0.0)  # Rojo.
    glLineWidth(2.0)  # Ajusta el grosor de la línea de la función seno.
    glBegin(GL_LINE_STRIP)
    for x in np.arange(-5, 5, 0.1):
        y = np.sin(x * np.pi)  # Multiplica x por pi para incrementar la frecuencia.
        glVertex3f(x, y, 0)
    glEnd()


# Bucle principal.
while True:
    for Evento in pygame.event.get():
        if Evento.type == pygame.QUIT:
            pygame.quit()
            quit()
    # Limpia la pantalla y establece el fondo en blanco.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1, 1, 1, 1)
    # Dibuja los ejes y la función seno.
    Dibujar_ejes()
    Dibujar_onda_sinusoidal()
    # Actualiza la pantalla.
    pygame.display.flip()
    pygame.time.wait(10)
