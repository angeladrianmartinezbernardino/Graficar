import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Inicialización de Pygame y OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glOrtho(0, 800, 600, 0, -1, 1)

# Cargar las texturas del sprite
sprite_frames = ["frame1.png", "frame2.png", "frame3.png", "frame4.png"]  # Añadir más si tienes más frames
textures = []

for frame in sprite_frames:
    surface = pygame.image.load(frame).convert_alpha()
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    textures.append((texture_id, width, height))

# Función para renderizar un frame
def render_frame(texture, width, height, x, y):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 1)
    glVertex2f(x, y + height)
    glEnd()
    glDisable(GL_TEXTURE_2D)

# Ciclo principal
clock = pygame.time.Clock()
frame_index = 0
x, y = 300, 200  # Posición del sprite

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar el frame actual
    texture, width, height = textures[frame_index]
    render_frame(texture, width, height, x, y)

    # Avanzar al siguiente frame
    frame_index = (frame_index + 1) % len(textures)

    pygame.display.flip()
    clock.tick(10)  # Cambia la velocidad de la animación ajustando los FPS

pygame.quit()
