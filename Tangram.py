import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *

class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((800,600),pg.OPENGL|pg.DOUBLEBUF)
        display = (800, 600)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -2)
        pg.display.set_caption("Tangram 2D con OpenGL movible con las teclas de dirección del teclado")
        self.clock = pg.time.Clock()
        glClearColor(0.0, 0.0, 0.0, 1)
        self.mainLoop()

    def mainLoop(self):
        rtri = 0.25
        running = True
        while (running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            #Triángulo grande verde oscuro.
            glColor3f(0,0.5,0)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(-0.5, 0.5, 0.0)
            glVertex3f(0.5, 0.5, 0.0)
            glEnd()
            # Triángulo grande naranja claro.
            glColor3f(1, 0.25, 0)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(-0.5, -0.5, 0.0)
            glVertex3f(-0.5, 0.5, 0.0)
            glEnd()
            # Triángulo pequeño rojo claro.
            glColor3f(1, 0, 0)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.25, 0.25, 0.0)
            glVertex3f(0.5, 0.5, 0.0)
            glVertex3f(0.5, 0.0, 0.0)
            glEnd()
            # Cuadrado amarillo claro.
            glColor3f(1, 1, 0)
            glBegin(GL_QUADS)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(0.25, 0.25, 0.0)
            glVertex3f(0.5, 0.0, 0.0)
            glVertex3f(0.25, -0.25, 0.0)
            glEnd()
            # Triángulo pequeño morado oscuro.
            glColor3f(0.5, 0, 1)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(0.25, -0.25, 0.0)
            glVertex3f(-0.25, -0.25, 0.0)
            glEnd()
            # Romboide azul oscuro.
            glColor3f(0, 0, 1)
            glBegin(GL_QUADS)
            glVertex3f(-0.25, -0.25, 0.0)
            glVertex3f(0.25, -0.25, 0.0)
            glVertex3f(0.0, -0.5, 0.0)
            glVertex3f(-0.5, -0.5, 0.0)
            glEnd()
            # Triángulo mediano rosa claro.
            glColor3f(1, 0, 1)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.5, 0.0, 0.0)
            glVertex3f(0.5, -0.5, 0.0)
            glVertex3f(0.0, -0.5, 0.0)
            glEnd()
            glFlush()
            # Refrescar pantalla.
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myApp = App()