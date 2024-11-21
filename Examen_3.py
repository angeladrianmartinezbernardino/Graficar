import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Variables globales para el movimiento de la esfera
sphere_y = 0.5  # Altura inicial de la esfera
move_speed = 0.05  # Velocidad de movimiento

def init():
    """Configuración inicial de OpenGL."""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

def display():
    """Función de renderizado."""
    global sphere_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(0.0, 1.0, 5.0,    # Posición del ojo
              0.0, 0.0, 0.0,    # Punto de referencia
              0.0, 1.0, 0.0)    # Vector "up"

    # Configuración de la fuente de luz
    light_pos = [1.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    # Dibujar una esfera roja usando gluSphere
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(0.0, sphere_y, 0.0)  # Actualiza la posición de la esfera
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.5, 50, 50)
    gluDeleteQuadric(quadric)  # Liberar recursos
    glPopMatrix()

    # Dibujar una base (rectángulo) en gris
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-1.0, -0.5, -1.0)
    glVertex3f(1.0, -0.5, -1.0)
    glVertex3f(1.0, -0.5, 1.0)
    glVertex3f(-1.0, -0.5, 1.0)
    glEnd()
    glPopMatrix()

    glfw.swap_buffers(window)

def reshape(window, width, height):
    """Ajuste del viewport y proyección cuando se cambia el tamaño de la ventana."""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / float(height or 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def key_callback(window, key, scancode, action, mods):
    """Callback para manejar los eventos de teclado."""
    global sphere_y, move_speed

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            sphere_y += move_speed  # Mover la esfera hacia arriba
        elif key == glfw.KEY_DOWN:
            sphere_y -= move_speed  # Mover la esfera hacia abajo

def main():
    """Configuración del entorno GLFW y ciclo principal."""
    global window

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Figura con Iluminación", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, reshape)
    glfw.set_key_callback(window, key_callback)  # Vincular el callback de teclado
    init()

    # Configuración inicial del viewport y proyección
    width, height = glfw.get_framebuffer_size(window)
    reshape(window, width, height)

    while not glfw.window_should_close(window):
        display()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
