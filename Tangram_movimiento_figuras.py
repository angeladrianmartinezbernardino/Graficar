import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *

class Figura:
    def __init__(self, Coordenadas_vertices, Color_figura):
        self.Coordenadas_vertices = Coordenadas_vertices
        self.Color_figura = Color_figura
        self.Figura_seleccionada = False

    def Dibujar(self):
        glColor3f(*self.Color_figura)
        if len(self.Coordenadas_vertices) == 3:
            glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_QUADS)
        for vertex in self.Coordenadas_vertices:
            glVertex3f(*vertex)
        glEnd()

    def Colision(self, x, y):
        Minimo_x = min(Vertice[0] for Vertice in self.Coordenadas_vertices)
        Maximo_x = max(Vertice[0] for Vertice in self.Coordenadas_vertices)
        Minimo_y = min(Vertice[1] for Vertice in self.Coordenadas_vertices)
        Maximo_y = max(Vertice[1] for Vertice in self.Coordenadas_vertices)
        return Minimo_x <= x <= Maximo_x and Minimo_y <= y <= Maximo_y

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
        pg.display.set_caption("Tangram 2D con OpenGL movible con las teclas de dirección del teclado")
        self.clock = pg.time.Clock()
        glClearColor(0.0, 0.0, 0.0, 1)
        # Crear las Figuras del tangram
        self.Figuras = [
            Figura([(0.0, 0.0, 0.0), (-0.5, 0.5, 0.0), (0.5, 0.5, 0.0)], (0, 0.5, 0)), # Triángulo grande verde oscuro.
            Figura([(0.0, 0.0, 0.0), (-0.5, -0.5, 0.0), (-0.5, 0.5, 0.0)], (1, 0.25, 0)), # Triángulo grande naranja claro.
            Figura([(0.25, 0.25, 0.0), (0.5, 0.5, 0.0), (0.5, 0.0, 0.0)], (1, 0, 0)), # Triángulo pequeño rojo claro.
            Figura([(0.0, 0.0, 0.0), (0.25, 0.25, 0.0), (0.5, 0.0, 0.0), (0.25, -0.25, 0.0)], (1, 1, 0)), # Cuadrado amarillo claro.
            Figura([(0.0, 0.0, 0.0), (0.25, -0.25, 0.0), (-0.25, -0.25, 0.0)], (0.5, 0, 1)), # Triángulo pequeño morado oscuro.
            Figura([(-0.25, -0.25, 0.0), (0.25, -0.25, 0.0), (0.0, -0.5, 0.0), (-0.5, -0.5, 0.0)], (0, 0, 1)), # Romboide azul oscuro.
            Figura([(0.5, 0.0, 0.0), (0.5, -0.5, 0.0), (0.0, -0.5, 0.0)], (1, 0, 1)) # Triángulo mediano rosa claro.
        ]
        self.Figura_seleccionada = None
        self.Bucle_principal()

    def Bucle_principal(self):
        running = True
        while running:
            for Evento in pg.event.get():
                if Evento.type == pg.QUIT:
                    running = False
                elif Evento.type == pg.MOUSEBUTTONDOWN:  # Selección con clic.
                    x, y = pg.mouse.get_pos()
                    # Convertir las coordenadas de la pantalla a coordenadas OpenGL.
                    x = (x / 400) - 1
                    y = 1 - (y / 300)
                    self.Seleccionar_figura(x, y)
                elif Evento.type == pg.KEYDOWN:  # Movimiento con teclas.
                    if self.Figura_seleccionada:
                        if Evento.key == pg.K_LEFT:
                            self.Figura_seleccionada.Mover_figura(-0.05, 0)
                        elif Evento.key == pg.K_RIGHT:
                            self.Figura_seleccionada.Mover_figura(0.05, 0)
                        elif Evento.key == pg.K_UP:
                            self.Figura_seleccionada.Mover_figura(0, 0.05)
                        elif Evento.key == pg.K_DOWN:
                            self.Figura_seleccionada.Mover_figura(0, -0.05)
            glClear(GL_COLOR_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            for figura in self.Figuras:
                figura.Dibujar()
            glFlush()
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def Seleccionar_figura(self, x, y):
        for Figura in self.Figuras:
            if Figura.Colision(x, y):
                self.Figura_seleccionada = Figura
                break

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myApp = App()
