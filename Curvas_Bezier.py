import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class App:
    def __init__(self):
        # inicilizar la ventana de pygame
        pg.init()
        #   tam vent    OPENGL    Buffer doble
        pg.display.set_mode((800, 800), pg.OPENGL | pg.DOUBLEBUF)
        display = (800, 800)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -2)
        pg.display.set_caption("Dibujar tangram 2D con OpenGL")
        self.clock = pg.time.Clock()  # controla el frame rate

        # iniciar opengl
        glClearColor(0.0, 0.0, 0.0, 1)  # color de fondo
        self.mainLoop()

    def setPixel(self,cx,cy,r,g,b):
        glPointSize(2)
        glBegin(GL_POINTS)
        glColor3f(r,g,b)
        glVertex2f(cx,cy)
        glEnd()
        glFlush()

    def mainLoop(self):
        dato =0
        LEFT = 1
        RIGHT = 3
        x=0
        y=0
        running = True
        while (running):
            #glClear(GL_COLOR_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            # checar eventos
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == LEFT:
                    x=event.pos[0]
                    x1 = (400 - x)/400 * -1
                    y=event.pos[1]
                    y1 = (400-y)/400
                    print(x1,y1)
                    self.setPixel(x1,y1,1,1,1)
                    print("You pressed the left mouse button at (%d, %d)" % event.pos)
                elif event.type == pg.MOUSEBUTTONUP and event.button == LEFT:
                    print("You released the left mouse button at (%d, %d)" % event.pos)
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == RIGHT:
                    print("You pressed the right mouse button at (%d, %d)" % event.pos)
                elif event.type == pg.MOUSEBUTTONUP and event.button == RIGHT:
                    print("You released the right mouse button at (%d, %d)" % event.pos)
            #glClear(GL_COLOR_BUFFER_BIT)
            #glMatrixMode(GL_MODELVIEW)
            x1 = 0.2
            y1 = 0.2
            x2 = 0.3
            y2 = 0.3
            x3 = -0.2
            y3 = -0.2
            x4 = 0.4
            y4 = -0.3
            a = 0
            b = 0
            t = 0.0
            while True:
                #a = ((((1-t)*(1-t))*x1)+((2*t)*(1-t)*x2)+((t*t)*x3))
                a=(x1*((1-t)*(1-t)*(1-t)))+(3*x2*t*((1-t)*(1-t)))+(3*x3*(t*t)*(1-t))+(x4*(t*t*t))
                b=(y1*((1-t)*(1-t)*(1-t)))+(3*y2*t*((1-t)*(1-t)))+(3*y3*(t*t)*(1-t))+(y4*(t*t*t))
                #b = ((((1-t)*(1-t))*y1)+((2*t)*(1-t)*y2)+((t*t)*y3))
                t+=0.001
                self.setPixel(a,b,1,0.5,1)
                if t>1:
                    break
            # refrescar pantalla
            pg.display.flip()

            # timing 60 cuadros por segundo
            self.clock.tick(60)
        self.quit()

    def quit(self):
        pg.quit()


if __name__ == "__main__":
    myApp = App()
