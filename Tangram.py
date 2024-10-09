# Practica 5 OpenGL tangram 2D
# Mi primer programa OpenGL
import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *

class App:

    def __init__(self):
        #inicilizar la ventana de pygame
        pg.init()
                        #   tam vent    OPENGL    Buffer doble
        pg.display.set_mode((800,600),pg.OPENGL|pg.DOUBLEBUF)
        display = (800, 600)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -2)
        pg.display.set_caption("Dibujar tangram 2D con OpenGL")
        self.clock = pg.time.Clock() # controla el frame rate

        #iniciar opengl
        glClearColor(0.0, 0.0, 0.0, 1) #color de fondo
        self.mainLoop()


    def mainLoop(self):
        rtri = 0.25
        running = True
        while (running):
            #checar eventos
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            #dibujar tangram 2D
            glClear(GL_COLOR_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)

            glColor3f(0,0.5,0)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.0, 0.0, 0.0) # Top
            glVertex3f(-0.5, 0.5, 0.0) # Bottom Left
            glVertex3f(0.5, 0.5, 0.0) # Bottom right
            glEnd()

            #glLoadIdentity()
            glColor3f(1, 0.25, 0)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.0, 0.0, 0.0)  # Top
            glVertex3f(-0.5, -0.5, 0.0)  # Bottom Left
            glVertex3f(-0.5, 0.5, 0.0)  # Bottom right
            glEnd()

            glColor3f(1, 0, 0)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.25, 0.25, 0.0)  # Top
            glVertex3f(0.5, 0.5, 0.0)  # Bottom Left
            glVertex3f(0.5, 0.0, 0.0)  # Bottom right
            glEnd()

            glColor3f(1, 1, 0)
            glBegin(GL_QUADS)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(0.25, 0.25, 0.0)
            glVertex3f(0.5, 0.0, 0.0)
            glVertex3f(0.25, -0.25, 0.0)
            glEnd()

            glColor3f(0.5, 0, 1)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.0, 0.0, 0.0)  # Top
            glVertex3f(0.25, -0.25, 0.0)  # Bottom Left
            glVertex3f(-0.25, -0.25, 0.0)  # Bottom right
            glEnd()

            glColor3f(0, 0, 1)
            glBegin(GL_QUADS)
            glVertex3f(-0.25, -0.25, 0.0)
            glVertex3f(0.25, -0.25, 0.0)
            glVertex3f(0.0, -0.5, 0.0)
            glVertex3f(-0.5, -0.5, 0.0)
            glEnd()

            glColor3f(1, 0, 1)
            glBegin(GL_TRIANGLES)
            glVertex3f(0.5, 0.0, 0.0)  # Top
            glVertex3f(0.5, -0.5, 0.0)  # Bottom Left
            glVertex3f(0.0, -0.5, 0.0)  # Bottom right
            glEnd()
            glFlush()

            #refrescar pantalla
            pg.display.flip()

            #timing 60 cuadros por segundo
            self.clock.tick(60)
        self.quit()

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myApp = App()