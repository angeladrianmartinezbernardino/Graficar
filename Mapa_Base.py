from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Nuevo Tecnológico.
ManuelOrozcoyBerra_IgnacioBorunda = (50, 500)
ManuelOrozcoyBerra_Topografos_Psicologos = (275, 500)

# Nuevo Tecnológico.
Topografos_Enfermeras = (275, 475)
Topografos_Antropologos = (275, 450)
Topografos_Disenadores = (275, 425)
Topografos_Veterinarios = (275, 400)
Topografos_AdministradoresPoniente = (300, 375)
Topografos_Sociologos = (325, 350)
Topografos_Geografos = (350, 325)
Topografos_Profesores = (350, 300)

# Nuevo Tecnológico.
ManuelOrozcoyBerra_SeizoFuruya = (400, 525)

# Nuevo Tecnológico.
SeizoFuruya_Psicologos = (400, 500)
SeizoFuruya_Enfermeras = (400, 475)
SeizoFuruya_Antropologos = (400, 450)
SeizoFuruya_Disenadores = (400, 425)
SeizoFuruya_Veterinarios = (400, 400)
SeizoFuruya_AdministradoresPoniente = (400, 375)
SeizoFuruya_Sociologos = (400, 350)
SeizoFuruya_Geografos = (400, 325)
SeizoFuruya_Profesores = (400, 300)

# Nuevo Tecnológico.
AntonioGarciaCubas_SeizoFuruya = (400, 50)
AntonioGarciaCubas_IgnacioBorunda = (50, 50)

# Resicencial Tecnológico.
AntonioGarciaCubas_PresaAlvaroObregon = (950, 50)
ManuelOrozcoyBerra_PresaAlvaroObregon = (1150, 550)

# Residencial Tecnológico.
ManuelOrozcoyBerra_Contadores = (450, 525)
AntonioGarciaCubas_Contadores = (450, 50)
ManuelOrozcoyBerra_Medicos = (500, 530)
AntonioGarciaCubas_Medicos = (500, 50)
ManuelOrozcoyBerra_Ingenieros = (550, 535)
AntonioGarciaCubas_Ingenieros = (550, 50)
ManuelOrozcoyBerra_Quimicos = (600, 540)

# Residencial Tecnológico.
X_Quimicos = (600, 50)
ManuelOrozcoyBerra_Fisicos = (650, 545)
X_Fisicos = (650, 50)
ManuelOrozcoyBerra_Biologos = (700, 550)
X_Biologos = (700, 50)
ManuelOrozcoyBerra_Ecologistas = (750, 555)
X_Ecologistas = (750, 50)

# Residencial Tecnológico.
SeizoFuruya_Industriales = (400, 460)
Industriales_Contadores = (450, 460)
Industriales_Medicos = (500, 460)
Industriales_Ingenieros = (550, 460)
Industriales_Quimicos = (600, 460)
Industriales_Fisicos = (650, 460)
Industriales_Biologos = (700, 460)
Industriales_Ecologistas = (750, 460)
Industriales_Arquitectos = (800, 460)

# Residencial Tecnológico.
Administradores_Contadores = (450, 375)
Administradores_Medicos = (500, 375)
Administradores_Ingenieros = (550, 375)
Administradores_Quimicos = (600, 375)
Administradores_Fisicos = (650, 375)
Administradores_Arquitectos = (750, 375)

# Residencial Tecnológico.
SeizoFuruya_Agronomos = (400, 290)
Agronomos_Contadores = (450, 290)
Agronomos_Medicos = (500, 290)
Agronomos_Ingenieros = (550, 290)

# Residencial Tecnológico.
ManuelOrozcoyBerra_Arquitectos = (850, 555)
AntonioGarciaCubas_Arquitectos = (600, 50)

I_A = (800, 460)
A_A = (700, 375)

# Calles definidas con origen y destino como variables.
Calles = {
    "Psicologos": {"origen": ManuelOrozcoyBerra_Topografos_Psicologos, "destino": SeizoFuruya_Psicologos, "nombre": "Psicólogos"},
    "Enfermeras": {"origen": Topografos_Enfermeras, "destino": SeizoFuruya_Enfermeras, "nombre": "Enfermeras"},
    "Antropologos": {"origen": Topografos_Antropologos, "destino": SeizoFuruya_Antropologos, "nombre": "Antropólogos"},
    "Disenadores": {"origen": Topografos_Disenadores, "destino": SeizoFuruya_Disenadores, "nombre": "Disenadores"},
    "Veterinarios": {"origen": Topografos_Veterinarios, "destino": SeizoFuruya_Veterinarios, "nombre": "Veterinarios"},
    "AdministradoresPoniente": {"origen": Topografos_AdministradoresPoniente, "destino": SeizoFuruya_AdministradoresPoniente, "nombre": "Administradores Poniente"},
    "Sociologos": {"origen": Topografos_Sociologos, "destino": SeizoFuruya_Sociologos, "nombre": "Sociólogos"},
    "Geografos": {"origen": Topografos_Geografos, "destino": SeizoFuruya_Geografos, "nombre": "Geógrafos"},
    "Profesores": {"origen": Topografos_Profesores, "destino": SeizoFuruya_Profesores, "nombre": "Profesores"},

    "Topografos": {"origen": ManuelOrozcoyBerra_Topografos_Psicologos, "destino": Topografos_Enfermeras, "nombre": "Topógrafos"},
    "Topografos2": {"origen": Topografos_Enfermeras, "destino": Topografos_Antropologos, "nombre": "Topógrafos"},
    "Topografos3": {"origen": Topografos_Antropologos, "destino": Topografos_Disenadores, "nombre": "Topógrafos"},
    "Topografos4": {"origen": Topografos_Disenadores, "destino": Topografos_Veterinarios, "nombre": "Topógrafos"},
    "Topografos5": {"origen": Topografos_Veterinarios, "destino": Topografos_AdministradoresPoniente, "nombre": "Topógrafos"},
    "Topografos6": {"origen": Topografos_AdministradoresPoniente, "destino": Topografos_Sociologos, "nombre": "Topógrafos"},
    "Topografos7": {"origen": Topografos_Sociologos, "destino": Topografos_Geografos, "nombre": "Topógrafos"},
    "Topografos8": {"origen": Topografos_Geografos, "destino": Topografos_Profesores, "nombre": "Topógrafos"},

    "AntonioGarciaCubas": {"origen": AntonioGarciaCubas_SeizoFuruya, "destino": AntonioGarciaCubas_IgnacioBorunda, "nombre": "Antonio García Cubas"},
    "AntonioGarciaCubas2": {"origen": AntonioGarciaCubas_SeizoFuruya, "destino": AntonioGarciaCubas_Contadores, "nombre": "Antonio García Cubas"},
    "AntonioGarciaCubas3": {"origen": AntonioGarciaCubas_Contadores, "destino": AntonioGarciaCubas_Medicos, "nombre": "Antonio García Cubas"},
    "AntonioGarciaCubas4": {"origen": AntonioGarciaCubas_Medicos, "destino": AntonioGarciaCubas_Ingenieros, "nombre": "Antonio García Cubas"},
    "AntonioGarciaCubas5": {"origen": AntonioGarciaCubas_Ingenieros, "destino": AntonioGarciaCubas_Arquitectos, "nombre": "Antonio García Cubas"},

    "IgnacioBorunda": {"origen": AntonioGarciaCubas_IgnacioBorunda, "destino": ManuelOrozcoyBerra_IgnacioBorunda, "nombre": "Ignacio Borunda"},

    "SeizoFuruya": {"origen": ManuelOrozcoyBerra_SeizoFuruya, "destino": SeizoFuruya_Psicologos, "nombre": "Seizo Furuya"},
    "SeizoFuruya2": {"origen": SeizoFuruya_Psicologos, "destino": SeizoFuruya_Enfermeras, "nombre": "Seizo Furuya"},
    "SeizoFuruya3": {"origen": SeizoFuruya_Enfermeras, "destino": SeizoFuruya_Antropologos, "nombre": "Seizo Furuya"},
    "SeizoFuruya4": {"origen": SeizoFuruya_Antropologos, "destino": SeizoFuruya_Disenadores, "nombre": "Seizo Furuya"},
    "SeizoFuruya5": {"origen": SeizoFuruya_Disenadores, "destino": SeizoFuruya_Veterinarios, "nombre": "Seizo Furuya"},
    "SeizoFuruya6": {"origen": SeizoFuruya_Veterinarios, "destino": SeizoFuruya_AdministradoresPoniente, "nombre": "Seizo Furuya"},
    "SeizoFuruya7": {"origen": SeizoFuruya_AdministradoresPoniente, "destino": SeizoFuruya_Sociologos, "nombre": "Seizo Furuya"},
    "SeizoFuruya8": {"origen": SeizoFuruya_Sociologos, "destino": SeizoFuruya_Geografos, "nombre": "Seizo Furuya"},
    "SeizoFuruya9": {"origen": SeizoFuruya_Geografos, "destino": SeizoFuruya_Profesores, "nombre": "Seizo Furuya"},
    "Seizo_Furuya10": {"origen": SeizoFuruya_Profesores, "destino": AntonioGarciaCubas_SeizoFuruya, "nombre": "Seizo Furuya"},

    # Residencial Tecnológico
    "ManuelOrozcoyBerra": {"origen": ManuelOrozcoyBerra_IgnacioBorunda, "destino": ManuelOrozcoyBerra_Topografos_Psicologos, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra2": {"origen": ManuelOrozcoyBerra_Topografos_Psicologos, "destino": ManuelOrozcoyBerra_SeizoFuruya, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra3": {"origen": ManuelOrozcoyBerra_SeizoFuruya, "destino": ManuelOrozcoyBerra_Contadores, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra4": {"origen": ManuelOrozcoyBerra_Contadores, "destino": ManuelOrozcoyBerra_Medicos, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra5": {"origen": ManuelOrozcoyBerra_Medicos, "destino": ManuelOrozcoyBerra_Ingenieros, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra6": {"origen": ManuelOrozcoyBerra_Ingenieros, "destino": ManuelOrozcoyBerra_Quimicos, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra7": {"origen": ManuelOrozcoyBerra_Quimicos, "destino": ManuelOrozcoyBerra_Fisicos, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra8": {"origen": ManuelOrozcoyBerra_Fisicos, "destino": ManuelOrozcoyBerra_Biologos, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra9": {"origen": ManuelOrozcoyBerra_Biologos, "destino": ManuelOrozcoyBerra_Ecologistas, "nombre": "Manuel Orozco y Berra"},
    "ManuelOrozcoyBerra10": {"origen": ManuelOrozcoyBerra_Ecologistas, "destino": ManuelOrozcoyBerra_Arquitectos, "nombre": "Manuel Orozco y Berra"},

    "Contadores": {"origen": ManuelOrozcoyBerra_Contadores, "destino": Industriales_Contadores, "nombre": "Contadores"},
    "Contadores2": {"origen": Industriales_Contadores, "destino": Administradores_Contadores, "nombre": "Contadores"},
    "Contadores3": {"origen": Administradores_Contadores, "destino": Agronomos_Contadores, "nombre": "Contadores"},
    "Contadores4": {"origen": Agronomos_Contadores, "destino": AntonioGarciaCubas_Contadores, "nombre": "Contadores"},
    "Medicos": {"origen": ManuelOrozcoyBerra_Medicos, "destino": Industriales_Medicos, "nombre": "Médicos"},
    "Medicos2": {"origen": Industriales_Medicos, "destino": Administradores_Medicos, "nombre": "Médicos"},
    "Medicos3": {"origen": Administradores_Medicos, "destino": Agronomos_Medicos, "nombre": "Médicos"},
    "Medicos4": {"origen": Agronomos_Medicos, "destino": AntonioGarciaCubas_Medicos, "nombre": "Médicos"},
    "Ingenieros": {"origen": ManuelOrozcoyBerra_Ingenieros, "destino": Industriales_Ingenieros, "nombre": "Ingenieros"},
    "Ingenieros2": {"origen": Industriales_Ingenieros, "destino": Administradores_Ingenieros, "nombre": "Ingenieros"},
    "Ingenieros3": {"origen": Administradores_Ingenieros, "destino": Agronomos_Ingenieros, "nombre": "Ingenieros"},
    "Ingenieros4": {"origen": Agronomos_Ingenieros, "destino": AntonioGarciaCubas_Ingenieros, "nombre": "Ingenieros"},
    "Quimicos": {"origen": ManuelOrozcoyBerra_Quimicos, "destino": Industriales_Quimicos, "nombre": "Químicos"},
    "Quimicos2": {"origen": Industriales_Quimicos, "destino": Administradores_Quimicos, "nombre": "Químicos"},
    "Fisicos": {"origen": ManuelOrozcoyBerra_Fisicos, "destino": Industriales_Fisicos, "nombre": "Físicos"},
    "Fisicos2": {"origen": Industriales_Fisicos, "destino": Administradores_Fisicos, "nombre": "Físicos"},
    "Biologos": {"origen": ManuelOrozcoyBerra_Biologos, "destino": Industriales_Biologos, "nombre": "Biólogos"},
    "Ecologistas": {"origen": ManuelOrozcoyBerra_Ecologistas, "destino": Industriales_Ecologistas, "nombre": "Ecologistas"},

    "Industriales": {"origen": SeizoFuruya_Industriales, "destino": Industriales_Contadores, "nombre": "Industriales"},
    "Industriales2": {"origen": Industriales_Contadores, "destino": Industriales_Medicos, "nombre": "Industriales"},
    "Industriales3": {"origen": Industriales_Medicos, "destino": Industriales_Ingenieros, "nombre": "Industriales"},
    "Industriales4": {"origen": Industriales_Ingenieros, "destino": Industriales_Quimicos, "nombre": "Industriales"},
    "Industriales5": {"origen": Industriales_Quimicos, "destino": Industriales_Fisicos, "nombre": "Industriales"},
    "Industriales6": {"origen": Industriales_Fisicos, "destino": Industriales_Biologos, "nombre": "Industriales"},
    "Industriales7": {"origen": Industriales_Biologos, "destino": Industriales_Ecologistas, "nombre": "Industriales"},
    "Industriales8": {"origen": Industriales_Ecologistas, "destino": Industriales_Arquitectos, "nombre": "Industriales"},

    "Administradores": {"origen": SeizoFuruya_AdministradoresPoniente, "destino": Administradores_Contadores, "nombre": "Administradores"},
    "Administradores2": {"origen": Administradores_Contadores, "destino": Administradores_Medicos, "nombre": "Administradores"},
    "Administradores3": {"origen": Administradores_Medicos, "destino": Administradores_Ingenieros, "nombre": "Administradores"},
    "Administradores4": {"origen": Administradores_Ingenieros, "destino": Administradores_Quimicos, "nombre": "Administradores"},
    "Administradores5": {"origen": Administradores_Quimicos, "destino": Administradores_Fisicos, "nombre": "Administradores"},
    "Administradores6": {"origen": Administradores_Fisicos, "destino": Administradores_Arquitectos, "nombre": "Administradores"},

    "Agronomos": {"origen": SeizoFuruya_Agronomos, "destino": Agronomos_Contadores, "nombre": "Agrónomos"},
    "Agronomos2": {"origen": Agronomos_Contadores, "destino": Agronomos_Medicos, "nombre": "Agrónomos"},
    "Agronomos3": {"origen": Agronomos_Medicos, "destino": Agronomos_Ingenieros, "nombre": "Agrónomos"},

    "Arquitectos": {"origen": ManuelOrozcoyBerra_Arquitectos, "destino": Industriales_Arquitectos, "nombre": "Arquitectos"},
    "Arquitectos2": {"origen": Industriales_Arquitectos, "destino": Administradores_Arquitectos, "nombre": "Arquitectos"},
    "Arquitectos3": {"origen": Administradores_Arquitectos, "destino": AntonioGarciaCubas_Arquitectos, "nombre": "Arquitectos"}
}

# Dimensiones de la ventana.
ancho_ventana = 900
alto_ventana = 600

# Función para dibujar un nodo.
def dibujar_nodo(x, y, size=5):
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = i * math.pi / 180  # Convierte grados a radianes.
        glVertex2f(x + size * math.cos(angle), y + size * math.sin(angle))
    glEnd()

# Función para dibujar una línea entre dos nodos.
def dibujar_linea(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

# Función para dibujar el grafo.
def dibujar_grafo():
    # Limpiar pantalla
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Dibuja las conexiones del grafo.
    glColor3f(0.0, 0.0, 1.0)  # Azul para las líneas.
    for calle in Calles.values():
        origen = calle["origen"]
        destino = calle["destino"]
        dibujar_linea(origen[0], origen[1], destino[0], destino[1])

    # Dibuja los nodos
    glColor3f(1.0, 0.0, 0.0)  # Rojo para los nodos.
    nodos = set()  # Para evitar dibujar nodos repetidos.
    for calle in Calles.values():
        nodos.add(calle["origen"])
        nodos.add(calle["destino"])
    for nodo in nodos:
        dibujar_nodo(nodo[0], nodo[1])

    glutSwapBuffers()

# Configuración inicial de OpenGL.
def inicializar_opengl():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Fondo blanco.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, ancho_ventana, 0, alto_ventana)  # Coordenadas 2D.
    glMatrixMode(GL_MODELVIEW)

# Configuración de la ventana GLUT.
def main():
    # Inicializar GLUT.
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(ancho_ventana, alto_ventana)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Prototipo de Mapa - Grafo en OpenGL")

    # Inicializar OpenGL.
    inicializar_opengl()

    # Configurar función de dibujo.
    glutDisplayFunc(dibujar_grafo)
    glutIdleFunc(dibujar_grafo)

    # Iniciar bucle principal.
    glutMainLoop()

# Ejecutar programa.
if __name__ == "__main__":
    main()
