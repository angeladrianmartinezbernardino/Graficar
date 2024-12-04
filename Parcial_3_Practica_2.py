import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Tamaño del tablero.
TAM_CELDA = 1

# Coordenadas del tablero.
def crear_tablero():
    tablero = []
    for x in range(3):
        for z in range(3):
            tablero.append((x, 0, z))
    return tablero

# Dibujar una celda.
def dibujar_celda(pos, color):
    x, y, z = pos
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex3f(x, y, z)
    glVertex3f(x + TAM_CELDA, y, z)
    glVertex3f(x + TAM_CELDA, y, z + TAM_CELDA)
    glVertex3f(x, y, z + TAM_CELDA)
    glEnd()

# Dibujar una ficha.
def dibujar_ficha(pos, color):
    x, y, z = pos
    glPushMatrix()
    glTranslatef(x + TAM_CELDA / 2, y + 0.1, z + TAM_CELDA / 2)
    glColor3fv(color)
    gluSphere(gluNewQuadric(), 0.3, 32, 32)
    glPopMatrix()

# Inicializar las fichas.
fichas = [
    {'pos': (0, 0, 0), 'color': (1, 1, 1)},  # Ficha blanca.
    {'pos': (2, 0, 2), 'color': (0, 0, 0)},  # Ficha negra.
]

# Mover una ficha.
def mover_ficha(ficha, nueva_pos):
    ficha['pos'] = nueva_pos

# Verificar si una ficha se "come" otra.
def verificar_comer(fichas):
    negras = [f for f in fichas if f['color'] == (0, 0, 0)]
    blancas = [f for f in fichas if f['color'] == (1, 1, 1)]
    for negra in negras:
        for blanca in blancas:
            if negra['pos'] == blanca['pos']:
                fichas.remove(blanca)
                print("¡La ficha negra se comió una ficha blanca!")

# Configuración inicial de OpenGL.
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-1.5, -2, -8)

    tablero = crear_tablero()
    seleccionada = fichas[1]  # Ficha negra seleccionada.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                x, y, z = seleccionada['pos']
                if event.key == K_LEFT:
                    nueva_pos = (x - 1, y, z)
                elif event.key == K_RIGHT:
                    nueva_pos = (x + 1, y, z)
                elif event.key == K_UP:
                    nueva_pos = (x, y, z - 1)
                elif event.key == K_DOWN:
                    nueva_pos = (x, y, z + 1)
                else:
                    continue

                # Limitar el movimiento dentro del tablero.
                if 0 <= nueva_pos[0] < 3 and 0 <= nueva_pos[2] < 3:
                    mover_ficha(seleccionada, nueva_pos)
                    verificar_comer(fichas)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar el tablero.
        for celda in tablero:
            color = (0.7, 0.7, 0.7) if (celda[0] + celda[2]) % 2 == 0 else (0.3, 0.3, 0.3)
            dibujar_celda(celda, color)

        # Dibujar las fichas.
        for ficha in fichas:
            dibujar_ficha(ficha['pos'], ficha['color'])

        pygame.display.flip()
        pygame.time.wait(100)

if __name__ == "__main__":
    main()
