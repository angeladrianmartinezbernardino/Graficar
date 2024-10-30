import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Figura:
    def __init__(self, Coordenadas_vertices, Color_figura):
        self.original_vertices = Coordenadas_vertices
        self.Color_figura = Color_figura
        self.Figura_seleccionada = False
        self.position = (0.0, 0.0)
        self.angle = 0.0

    def get_transformed_vertices(self):
        transformed_vertices = []
        cos_angle = math.cos(math.radians(self.angle))
        sin_angle = math.sin(math.radians(self.angle))
        for x0, y0, z0 in self.original_vertices:
            # Aplicar rotación
            x_rot = x0 * cos_angle - y0 * sin_angle
            y_rot = x0 * sin_angle + y0 * cos_angle
            # Aplicar traslación
            x = x_rot + self.position[0]
            y = y_rot + self.position[1]
            z = z0
            transformed_vertices.append((x, y, z))
        return transformed_vertices

    def Dibujar(self):
        glColor3f(*self.Color_figura)
        if len(self.original_vertices) == 3:
            glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_QUADS)
        for vertex in self.get_transformed_vertices():
            glVertex3f(*vertex)
        glEnd()

    def Mover_figura(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def Rotar_figura(self, incremento_angulo):
        self.angle += incremento_angulo
        self.angle %= 360

    def Colision(self, x, y):
        transformed_vertices = [(vx, vy) for vx, vy, vz in self.get_transformed_vertices()]
        return self.punto_en_poligono(x, y, transformed_vertices)

    def punto_en_poligono(self, x, y, poligono):
        num = len(poligono)
        j = num - 1
        c = False
        for i in range(num):
            xi, yi = poligono[i]
            xj, yj = poligono[j]
            if ((yi > y) != (yj > y)) and \
               (x < (xj - xi) * (y - yi) / (yj - yi + 1e-10) + xi):
                c = not c
            j = i
        return c

    def colision_con_otro(self, otra_figura):
        poly1 = self.get_transformed_vertices()
        poly2 = otra_figura.get_transformed_vertices()
        # Verificar si los bordes se intersectan
        for i in range(len(poly1)):
            p1 = poly1[i]
            p2 = poly1[(i+1)%len(poly1)]
            for j in range(len(poly2)):
                q1 = poly2[j]
                q2 = poly2[(j+1)%len(poly2)]
                if self.segmentos_se_intersectan(p1, p2, q1, q2):
                    return True
        # Verificar si algún vértice de poly1 está dentro de poly2
        for x, y, z in poly1:
            if otra_figura.punto_en_poligono(x, y, [(vx, vy) for vx, vy, vz in poly2]):
                return True
        # Verificar si algún vértice de poly2 está dentro de poly1
        for x, y, z in poly2:
            if self.punto_en_poligono(x, y, [(vx, vy) for vx, vy, vz in poly1]):
                return True
        return False

    def segmentos_se_intersectan(self, p1, p2, q1, q2):
        # Retorna True si los segmentos de línea p1-p2 y q1-q2 se intersectan
        def orientacion(a, b, c):
            # Retorna 0 si es colineal, 1 si es horario, 2 si es antihorario
            val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
            if abs(val) < 1e-10:
                return 0
            elif val > 0:
                return 1
            else:
                return 2

        def en_segmento(a, b, c):
            if min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and \
               min(a[1], b[1]) <= c[1] <= max(a[1], b[1]):
                return True
            return False

        A = (p1[0], p1[1])
        B = (p2[0], p2[1])
        C = (q1[0], q1[1])
        D = (q2[0], q2[1])

        o1 = orientacion(A, B, C)
        o2 = orientacion(A, B, D)
        o3 = orientacion(C, D, A)
        o4 = orientacion(C, D, B)

        if o1 != o2 and o3 != o4:
            return True

        # Casos especiales
        if o1 == 0 and en_segmento(A, B, C):
            return True
        if o2 == 0 and en_segmento(A, B, D):
            return True
        if o3 == 0 and en_segmento(C, D, A):
            return True
        if o4 == 0 and en_segmento(C, D, B):
            return True

        return False

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
        # Crear las figuras del tangram
        self.Figuras = [
            Figura([(0.0, 0.0, 0.0), (-0.5, 0.5, 0.0), (0.5, 0.5, 0.0)], (0, 0.5, 0)),  # Triángulo grande verde oscuro
            Figura([(0.0, 0.0, 0.0), (-0.5, -0.5, 0.0), (-0.5, 0.5, 0.0)], (1, 0.25, 0)),  # Triángulo grande naranja claro
            Figura([(0.25, 0.25, 0.0), (0.5, 0.5, 0.0), (0.5, 0.0, 0.0)], (1, 0, 0)),  # Triángulo pequeño rojo claro
            Figura([(0.0, 0.0, 0.0), (0.25, 0.25, 0.0), (0.5, 0.0, 0.0), (0.25, -0.25, 0.0)], (1, 1, 0)),  # Cuadrado amarillo claro
            Figura([(0.0, 0.0, 0.0), (0.25, -0.25, 0.0), (-0.25, -0.25, 0.0)], (0.5, 0, 1)),  # Triángulo pequeño morado oscuro
            Figura([(-0.25, -0.25, 0.0), (0.25, -0.25, 0.0), (0.0, -0.5, 0.0), (-0.5, -0.5, 0.0)], (0, 0, 1)),  # Romboide azul oscuro
            Figura([(0.5, 0.0, 0.0), (0.5, -0.5, 0.0), (0.0, -0.5, 0.0)], (1, 0, 1))  # Triángulo mediano rosa claro
        ]
        self.Figura_seleccionada = None
        self.Bucle_principal()

    def Bucle_principal(self):
        running = True
        while running:
            for Evento in pg.event.get():
                if Evento.type == pg.QUIT:
                    running = False
                elif Evento.type == pg.MOUSEBUTTONDOWN:  # Selección con clic
                    x, y = pg.mouse.get_pos()
                    # Convertir coordenadas de pantalla a OpenGL
                    x = (x / 400) - 1
                    y = 1 - (y / 300)
                    self.Seleccionar_figura(x, y)

            # Obtener el estado actual de todas las teclas
            keys = pg.key.get_pressed()

            if self.Figura_seleccionada:
                dx = dy = 0
                rotar_angulo = 0

                # Movimiento con teclas de dirección
                if keys[pg.K_LEFT]:
                    dx = -0.005  # Puedes ajustar la velocidad de movimiento
                if keys[pg.K_RIGHT]:
                    dx = 0.005
                if keys[pg.K_UP]:
                    dy = 0.005
                if keys[pg.K_DOWN]:
                    dy = -0.005

                # Rotación con teclas 'L' y 'R'
                if keys[pg.K_l]:
                    rotar_angulo = -0.1  # Ajusta el ángulo de rotación si es necesario
                if keys[pg.K_r]:
                    rotar_angulo = 0.1

                # Mover figura y verificar colisiones
                if dx != 0 or dy != 0:
                    self.Figura_seleccionada.Mover_figura(dx, dy)
                    colision = False
                    for figura in self.Figuras:
                        if figura != self.Figura_seleccionada:
                            if self.Figura_seleccionada.colision_con_otro(figura):
                                colision = True
                                break
                    if colision:
                        # Revertir movimiento si hay colisión
                        self.Figura_seleccionada.Mover_figura(-dx, -dy)

                # Rotar figura y verificar colisiones
                if rotar_angulo != 0:
                    self.Figura_seleccionada.Rotar_figura(rotar_angulo)
                    colision = False
                    for figura in self.Figuras:
                        if figura != self.Figura_seleccionada:
                            if self.Figura_seleccionada.colision_con_otro(figura):
                                colision = True
                                break
                    if colision:
                        # Revertir rotación si hay colisión
                        self.Figura_seleccionada.Rotar_figura(-rotar_angulo)

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
