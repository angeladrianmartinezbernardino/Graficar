import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *

class Figura:
    def __init__(self, Coordenadas_vertices, Color_figura):
        self.Coordenadas_vertices = Coordenadas_vertices
        self.Color_figura = Color_figura
        self.Figura_seleccionada = False

    def dibujar(self):
        glColor3f(*self.Color_figura)
        if len(self.Coordenadas_vertices) == 3:
            glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_QUADS)

        for vertex in self.Coordenadas_vertices:
            glVertex3f(*vertex)
        glEnd()

    def colision(self, x, y):
        min_x = min(v[0] for v in self.Coordenadas_vertices)
        max_x = max(v[0] for v in self.Coordenadas_vertices)
        min_y = min(v[1] for v in self.Coordenadas_vertices)
        max_y = max(v[1] for v in self.Coordenadas_vertices)
        return min_x <= x <= max_x and min_y <= y <= max_y

    def Mover_figura(self, dx, dy):
        for i in range(len(self.Coordenadas_vertices)):
            self.Coordenadas_vertices[i] = (self.Coordenadas_vertices[i][0] + dx, self.Coordenadas_vertices[i][1] + dy, self.Coordenadas_vertices[i][2])

class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        display = (800, 600)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -2)
        pg.display.set_caption("Dibujar tangram 2D con OpenGL")
        self.clock = pg.time.Clock()
        glClearColor(0.0, 0.0, 0.0, 1)

        # Crear las figuras del tangram
        self.figuras = [
            Figura([(0.0, 0.0, 0.0), (-0.5, 0.5, 0.0), (0.5, 0.5, 0.0)], (0, 0.5, 0)), # Triángulo grande verde oscuro.
            Figura([(0.0, 0.0, 0.0), (-0.5, -0.5, 0.0), (-0.5, 0.5, 0.0)], (1, 0.25, 0)), # Triángulo grande naranja claro.
            Figura([(0.25, 0.25, 0.0), (0.5, 0.5, 0.0), (0.5, 0.0, 0.0)], (1, 0, 0)), # Triángulo pequeño rojo claro.
            Figura([(0.0, 0.0, 0.0), (0.25, 0.25, 0.0), (0.5, 0.0, 0.0), (0.25, -0.25, 0.0)], (1, 1, 0)), # Cuadrado amarillo claro.
            Figura([(0.0, 0.0, 0.0), (0.25, -0.25, 0.0), (-0.25, -0.25, 0.0)], (0.5, 0, 1)), # Triángulo pequeño morado oscuro.
            Figura([(-0.25, -0.25, 0.0), (0.25, -0.25, 0.0), (0.0, -0.5, 0.0), (-0.5, -0.5, 0.0)], (0, 0, 1)), # Romboide azul oscuro.
            Figura([(0.5, 0.0, 0.0), (0.5, -0.5, 0.0), (0.0, -0.5, 0.0)], (1, 0, 1)) # Triángulo mediano rosa claro.
        ]

        self.figura_seleccionada = None  # Para almacenar la figura Figura_seleccionada
        self.mainLoop()

    def mainLoop(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:  # Selección con clic
                    x, y = pg.mouse.get_pos()
                    # Convertir las coordenadas de la pantalla a coordenadas OpenGL
                    x = (x / 400) - 1
                    y = 1 - (y / 300)
                    self.seleccionar_figura(x, y)
                elif event.type == pg.KEYDOWN:  # Movimiento con teclas
                    if self.figura_seleccionada:
                        if event.key == pg.K_LEFT:
                            self.figura_seleccionada.Mover_figura(-0.05, 0)
                        elif event.key == pg.K_RIGHT:
                            self.figura_seleccionada.Mover_figura(0.05, 0)
                        elif event.key == pg.K_UP:
                            self.figura_seleccionada.Mover_figura(0, 0.05)
                        elif event.key == pg.K_DOWN:
                            self.figura_seleccionada.Mover_figura(0, -0.05)

            glClear(GL_COLOR_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)

            # Dibujar todas las figuras
            for figura in self.figuras:
                figura.dibujar()

            glFlush()
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def seleccionar_figura(self, x, y):
        for figura in self.figuras:
            if figura.colision(x, y):
                self.figura_seleccionada = figura
                break

    def quit(self):
        pg.quit()


if __name__ == "__main__":
    myApp = App()
