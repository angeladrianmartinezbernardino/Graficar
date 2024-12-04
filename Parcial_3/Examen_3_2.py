import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *

# Inicialización de Pygame y OpenGL.
pygame.init()
pantalla = (800, 600)
pygame.display.set_mode(pantalla, DOUBLEBUF | OPENGL)
glOrtho(0, 800, 0, 600, -1, 1)

# Establecer el color de fondo a blanco.
glClearColor(1.0, 1.0, 1.0, 1.0)

# Cargar las texturas del sprite.
fotogramas_sprite = [
    "Shepherd_default.png",
    "Shepherd_walk_1.png",
    "Shepherd_walk_2.png",
    "Shepherd_walk_3.png",
    "Shepherd_walk_4.png",
    "Shepherd_walk_5.png",
    "Shepherd_walk_6.png",
    "Shepherd_bark_1.png",
    "Shepherd_bark_2.png",
    "Shepherd_bark_3.png",
    "Shepherd_run_1.png",
    "Shepherd_run_2.png",
    "Shepherd_run_3.png",
    "Shepherd_run_4.png",
    "Shepherd_run_5.png"
]  # Añadir más si tienes más fotogramas.
texturas = []

for fotograma in fotogramas_sprite:
    superficie = pygame.image.load(fotograma).convert_alpha()
    datos_textura = pygame.image.tostring(superficie, "RGBA", False)
    ancho, alto = superficie.get_size()

    id_textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id_textura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0, GL_RGBA, GL_UNSIGNED_BYTE, datos_textura)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    texturas.append((id_textura, ancho, alto))

# Función para renderizar un fotograma.
def renderizar_fotograma(textura, ancho, alto, x, y):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(x, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + ancho, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + ancho, y + alto)
    glTexCoord2f(0, 0)
    glVertex2f(x, y + alto)
    glEnd()
    glDisable(GL_TEXTURE_2D)

# Ciclo principal.
reloj = pygame.time.Clock()
indice_fotograma = 0
x, y = 300, 200  # Posición del sprite.

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar el fotograma actual.
    textura, ancho, alto = texturas[indice_fotograma]
    renderizar_fotograma(textura, ancho, alto, x, y)

    # Avanzar al siguiente fotograma.
    indice_fotograma = (indice_fotograma + 1) % len(texturas)

    pygame.display.flip()
    reloj.tick(10)  # Cambia la velocidad de la animación ajustando los FPS.

pygame.quit()
