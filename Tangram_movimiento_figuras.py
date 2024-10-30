import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Figura:
    def __init__(self, Coordenadas_vertices, Color_figura):
        self.Original_vertices = Coordenadas_vertices
        self.Color_figura = Color_figura
        self.Figura_seleccionada = False
        self.Posicion = (0.0, 0.0)
        self.Angulo = 0.0

    def Obtener_vertices_trnsformados(self):
        Vertices_transformados = []
        Angulo_coseno = math.cos(math.radians(self.Angulo))
        Angulo_seno = math.sin(math.radians(self.Angulo))
        for x0, y0, z0 in self.Original_vertices:
            # Aplicar rotación.
            Rotacion_x = x0 * Angulo_coseno - y0 * Angulo_seno
            Rotacion_y = x0 * Angulo_seno + y0 * Angulo_coseno
            # Aplicar traslación.
            x = Rotacion_x + self.Posicion[0]
            y = Rotacion_y + self.Posicion[1]
            z = z0
            Vertices_transformados.append((x, y, z))
        return Vertices_transformados

    def Dibujar(self):
        glColor3f(*self.Color_figura)
        if len(self.Original_vertices) == 3:
            glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_QUADS)
        for vertex in self.Obtener_vertices_trnsformados():
            glVertex3f(*vertex)
        glEnd()

    def Mover_figura(self, dx, dy):
        self.Posicion = (self.Posicion[0] + dx, self.Posicion[1] + dy)

    def Rotar_figura(self, Incremento_angulo):
        self.Angulo += Incremento_angulo
        self.Angulo %= 360

    def Colision(self, x, y):
        transformed_vertices = [(vx, vy) for vx, vy, vz in self.Obtener_vertices_trnsformados()]
        return self.Punto_en_poligono(x, y, transformed_vertices)

    def Punto_en_poligono(self, x, y, Poligono):
        Numero = len(Poligono)
        j = Numero - 1
        c = False
        for i in range(Numero):
            xi, yi = Poligono[i]
            xj, yj = Poligono[j]
            if ((yi > y) != (yj > y)) and \
               (x < (xj - xi) * (y - yi) / (yj - yi + 1e-10) + xi):
                c = not c
            j = i
        return c

    def Colision_con_otra_figura(self, Otra_figura):
        Poligono_1 = self.Obtener_vertices_trnsformados()
        Poligono_2 = Otra_figura.Obtener_vertices_trnsformados()
        # Verificar si los bordes se intersectan.
        for i in range(len(Poligono_1)):
            P1 = Poligono_1[i]
            P2 = Poligono_1[(i+1)%len(Poligono_1)]
            for j in range(len(Poligono_2)):
                Q1 = Poligono_2[j]
                Q2 = Poligono_2[(j+1)%len(Poligono_2)]
                if self.Segmentos_se_intersectan(P1, P2, Q1, Q2):
                    return True
        # Verificar si algún vértice de Poligono_1 está dentro de Poligono_2.
        for x, y, z in Poligono_1:
            if Otra_figura.Punto_en_poligono(x, y, [(vx, vy) for vx, vy, vz in Poligono_2]):
                return True
        # Verificar si algún vértice de Poligono_2 está dentro de Poligono_1.
        for x, y, z in Poligono_2:
            if self.Punto_en_poligono(x, y, [(vx, vy) for vx, vy, vz in Poligono_1]):
                return True
        return False

    def Segmentos_se_intersectan(self, P1, P2, Q1, Q2):
        # Retorna True si los segmentos de línea P1-P2 y Q1-Q2 se intersectan.
        def Orientacion(A, B, C):
            # Retorna 0 si es colineal, 1 si es horario, 2 si es antihorario.
            Valor = (B[1] - A[1]) * (C[0] - B[0]) - (B[0] - A[0]) * (C[1] - B[1])
            if abs(Valor) < 1e-10:
                return 0
            elif Valor > 0:
                return 1
            else:
                return 2
        def En_segmento(A, B, C):
            if min(A[0], B[0]) <= C[0] <= max(A[0], B[0]) and \
               min(A[1], B[1]) <= C[1] <= max(A[1], B[1]):
                return True
            return False
        A = (P1[0], P1[1])
        B = (P2[0], P2[1])
        C = (Q1[0], Q1[1])
        D = (Q2[0], Q2[1])
        O1 = Orientacion(A, B, C)
        O2 = Orientacion(A, B, D)
        O3 = Orientacion(C, D, A)
        O4 = Orientacion(C, D, B)
        if O1 != O2 and O3 != O4:
            return True
        # Casos especiales.
        if O1 == 0 and En_segmento(A, B, C):
            return True
        if O2 == 0 and En_segmento(A, B, D):
            return True
        if O3 == 0 and En_segmento(C, D, A):
            return True
        if O4 == 0 and En_segmento(C, D, B):
            return True
        return False

class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        Pantalla = (800, 600)
        gluPerspective(45, (Pantalla[0] / Pantalla[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -2)
        pg.display.set_caption("Tangram 2D con OpenGL movible con las teclas de dirección del teclado")
        self.clock = pg.time.Clock()
        glClearColor(0.0, 0.0, 0.0, 1)
        # Crear las figuras del tangram.
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
        Ejecucion = True
        while Ejecucion:
            for Evento in pg.event.get():
                if Evento.type == pg.QUIT:
                    Ejecucion = False
                elif Evento.type == pg.MOUSEBUTTONDOWN:  # Selección con clic.
                    x, y = pg.mouse.get_pos()
                    # Convertir coordenadas de pantalla a OpenGL.
                    x = (x / 400) - 1
                    y = 1 - (y / 300)
                    self.Seleccionar_figura(x, y)
            # Obtener el estado actual de todas las teclas.
            keys = pg.key.get_pressed()
            if self.Figura_seleccionada:
                dx = dy = 0
                Rotar_angulo = 0
                # Movimiento con teclas de dirección.
                if keys[pg.K_LEFT]:
                    dx = -0.005  # Puedes ajustar la velocidad de movimiento.
                if keys[pg.K_RIGHT]:
                    dx = 0.005  # Puedes ajustar la velocidad de movimiento.
                if keys[pg.K_UP]:
                    dy = 0.005  # Puedes ajustar la velocidad de movimiento.
                if keys[pg.K_DOWN]:
                    dy = -0.005  # Puedes ajustar la velocidad de movimiento.
                # Rotación con teclas "L" y "R".
                if keys[pg.K_l]:
                    Rotar_angulo = -0.1  # Ajusta el ángulo de rotación si es necesario.
                if keys[pg.K_r]:
                    Rotar_angulo = 0.1  # Ajusta el ángulo de rotación si es necesario.
                # Mover figura y verificar colisiones.
                if dx != 0 or dy != 0:
                    self.Figura_seleccionada.Mover_figura(dx, dy)
                    Colision = False
                    for Figura in self.Figuras:
                        if Figura != self.Figura_seleccionada:
                            if self.Figura_seleccionada.Colision_con_otra_figura(Figura):
                                Colision = True
                                break
                    if Colision:
                        # Revertir movimiento si hay colisión.
                        self.Figura_seleccionada.Mover_figura(-dx, -dy)
                # Rotar figura y verificar colisiones.
                if Rotar_angulo != 0:
                    self.Figura_seleccionada.Rotar_figura(Rotar_angulo)
                    Colision = False
                    for Figura in self.Figuras:
                        if Figura != self.Figura_seleccionada:
                            if self.Figura_seleccionada.Colision_con_otra_figura(Figura):
                                Colision = True
                                break
                    if Colision:
                        # Revertir rotación si hay colisión.
                        self.Figura_seleccionada.Rotar_figura(-Rotar_angulo)
            glClear(GL_COLOR_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            for Figura in self.Figuras:
                Figura.Dibujar()
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
