import sys
import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image  

zoom = -100.0
zoom_speed = 5.0

# Función de teclado para controlar el zoom.
def specialKeys(key, x, y):
    global zoom
    if key == GLUT_KEY_UP:
        zoom += zoom_speed
    elif key == GLUT_KEY_DOWN:
        zoom -= zoom_speed

# Función para cargar la textura desde un archivo de imagen.
def loadTexture(filename):
    img = Image.open(filename)
    img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    width, height = img.size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texture_id

# Función para dibujar una esfera con textura.
def drawTexturedSphere(texture_id, radius, slices, stacks):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)
    glDisable(GL_TEXTURE_2D)

# Función para configurar la proyección.
def set_projection(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = w / h
    gluPerspective(45, aspect_ratio, 1, 2000)  # Incrementamos el límite de visión.
    glMatrixMode(GL_MODELVIEW)

def drawOrbits():
    glColor3f(0.5, 0.5, 0.5)  # Color gris para las órbitas.
    glLineWidth(1.0)  # Ancho de línea

    # Órbita de Mercurio.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(200.0 * math.cos(angle), 0.0, -200.0 * math.sin(angle))
    glEnd()

    # Órbita de Venus.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(250.0 * math.cos(angle), 0.0, -250.0 * math.sin(angle))
    glEnd()

    # Órbita de la Tierra.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(300.0 * math.cos(angle), 0.0, -300.0 * math.sin(angle))
    glEnd()

    # Órbita de Marte.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(350.0 * math.cos(angle), 0.0, -350.0 * math.sin(angle))
    glEnd()

    # Órbita de Júpiter.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(400.0 * math.cos(angle), 0.0, -400.0 * math.sin(angle))
    glEnd()

    # Órbita de Saturno.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(450.0 * math.cos(angle), 0.0, -450.0 * math.sin(angle))
    glEnd()

    # Órbita de Urano.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(500.0 * math.cos(angle), 0.0, -500.0 * math.sin(angle))
    glEnd()

    # Órbita de Neptuno.
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(550.0 * math.cos(angle), 0.0, -550.0 * math.sin(angle))
    glEnd()

def drawBackgroundSphere(radius, slices, stacks):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, background_texture)  # Suponiendo que tienes una textura para el fondo de estrellas.
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)

# Función para dibujar los planetas.
def drawPlanets():
    # Sol
    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glRotatef(angle_sun, 0, 1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, sun_texture)
    drawTexturedSphere(sun_texture, 50.0, 20, 20)
    glPopMatrix()

    # Mercurio.
    glColor3f(0.8, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(200.0 * math.cos(math.radians(angle_mercury)), 0.0, -200.0 * math.sin(math.radians(angle_mercury)))  # Orbitar alrededor del sol.
    glRotatef(angle_mercury, 0, 1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, mercury_texture)
    drawTexturedSphere(mercury_texture, 7.0, 20, 20)
    glPopMatrix()

    # Venus.
    glColor3f(0.9, 0.6, 0.0)
    glPushMatrix()
    glTranslatef(250.0 * math.cos(math.radians(angle_venus)), 0.0, -250.0 * math.sin(math.radians(angle_venus)))  # Orbitar alrededor del sol.
    glRotatef(angle_venus, 0, 1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, venus_texture)
    drawTexturedSphere(venus_texture, 9.0, 20, 20)
    glPopMatrix()

    # Tierra.
    glColor3f(0.0, 0.5, 1.0)
    glPushMatrix()
    glTranslatef(300.0 * math.cos(math.radians(angle_earth)), 0.0, -300.0 * math.sin(math.radians(angle_earth)))  # Orbitar alrededor del sol.
    glRotatef(angle_earth, 1, -1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, earth_texture)
    drawTexturedSphere(earth_texture, 10, 20, 20)
    glPopMatrix()

    # Luna.
    glColor3f(200, 200, 200)
    glPushMatrix()
    glTranslatef(300.0 * math.cos(math.radians(angle_earth)), 0.0, -300.0 * math.sin(math.radians(angle_earth)))  # Orbitar alrededor del sol.
    glTranslatef(20.0 * math.cos(math.radians(angle_earth + angle_luna)), 0.0, -20.0 * math.sin(math.radians(angle_earth + angle_luna)))  # Orbitar alrededor de la tierra.
    glRotatef(angle_luna, 0, 1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Luna_texture)
    drawTexturedSphere(Luna_texture, 4.5, 20, 20)
    glPopMatrix()

    # Marte.
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(350.0 * math.cos(math.radians(angle_mars)), 0.0, -350.0 * math.sin(math.radians(angle_mars)))  # Orbitar alrededor del sol.
    glRotatef(angle_mars, 1, -1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, mars_texture)
    drawTexturedSphere(mars_texture, 10, 20, 20)
    glPopMatrix()

    # Luna 1 de Marte (Fobos).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(350.0 * math.cos(math.radians(angle_mars)), 0.0, -350.0 * math.sin(math.radians(angle_mars)))  # Orbitar alrededor del sol.
    glTranslatef(20.0 * math.cos(math.radians(angle_mars + angle_luna)), 0.0, -20.0 * math.sin(math.radians(angle_mars + angle_luna)))  # Orbitar alrededor de Marte.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Fobos)  # Textura de la Luna.
    drawTexturedSphere(Fobos, 3.0, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Luna 2 de Marte (Deimos).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(350.0 * math.cos(math.radians(angle_mars)), 0.0, -350.0 * math.sin(math.radians(angle_mars)))  # Orbitar alrededor del sol.
    glTranslatef(-30.0 * math.cos(math.radians(angle_mars + angle_luna)), 0.0, +30.0 * math.sin(math.radians(angle_mars + angle_luna)))  # Orbitar alrededor de Marte.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Deimos)  # Textura de la Luna.
    drawTexturedSphere(Deimos, 2.5, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    #Anillo de asteorides.
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(375.0 * math.cos(math.radians(angle_ast)), 0.0, -375.0 * math.sin(math.radians(angle_ast)))  # Orbitar alrededor del sol.
    glRotatef(angle_ast, 0, 1, 0)  # Rotación del asteroide alrededor del eje Y.
    glBindTexture(GL_TEXTURE_2D, As_texture)
    drawTexturedSphere(As_texture, 2.5, 20, 20)
    glPopMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(380.0 * math.cos(math.radians(angle_ast)), 0.0, -376.0 * math.sin(math.radians(angle_ast)))  # Orbitar alrededor del sol.
    glRotatef(angle_ast, 0, 1, 0)  # Rotación del asteroide alrededor del eje Y.
    glBindTexture(GL_TEXTURE_2D, As_texture)
    drawTexturedSphere(As_texture, 2.5, 20, 20)
    glPopMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(385.0 * math.cos(math.radians(angle_ast)), 0.0, -377.0 * math.sin(math.radians(angle_ast)))  # Orbitar alrededor del sol.
    glRotatef(angle_ast, 0, 1, 0)  # Rotación del asteroide alrededor del eje Y.
    glBindTexture(GL_TEXTURE_2D, As_texture)
    drawTexturedSphere(As_texture, 2.5, 20, 20)
    glPopMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(390.0 * math.cos(math.radians(angle_ast)), 0.0, -378.0 * math.sin(math.radians(angle_ast)))  # Orbitar alrededor del sol.
    glRotatef(angle_ast, 0, 1, 0)  # Rotación del asteroide alrededor del eje Y.
    glBindTexture(GL_TEXTURE_2D, As_texture)
    drawTexturedSphere(As_texture, 2.5, 20, 20)
    glPopMatrix()

    # Jupiter.
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(400.0 * math.cos(math.radians(angle_Jupiter)), 0.0, -400.0 * math.sin(math.radians(angle_Jupiter)))  # Orbitar alrededor del sol.
    glRotatef(angle_Jupiter, 0, 1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Jupiter_texture)
    drawTexturedSphere(Jupiter_texture, 25, 20, 20)
    glPopMatrix()

    # Luna 1 de Júpiter (Ío).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(400.0 * math.cos(math.radians(angle_Jupiter)) + 60.0 * math.cos(math.radians(angle_luna)), 0.0, -400.0 * math.sin(math.radians(angle_Jupiter)) - 30.0 * math.sin(math.radians(angle_luna)))  # Orbitar alrededor de Júpiter.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Io)  # Textura de la Luna.
    drawTexturedSphere(Io, 4.0, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Luna 2 de Júpiter (Europa).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(400.0 * math.cos(math.radians(angle_Jupiter)) + 40.0 * math.cos(math.radians(angle_luna)), 0.0, -400.0 * math.sin(math.radians(angle_Jupiter)) - 40.0 * math.sin(math.radians(angle_luna)))  # Orbitar alrededor de Júpiter.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Europa)  # Textura de la Luna.
    drawTexturedSphere(Europa, 4.0, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Saturno.
    glColor3f(0.5, 0.5, 0.5)  # Color amarillo dorado para Saturno.
    glPushMatrix()
    glTranslatef(450.0 * math.cos(math.radians(angle_Saturno)), 0.0, -450.0 * math.sin(math.radians(angle_Saturno)))  # Orbitar alrededor del sol.
    glRotatef(angle_Jupiter, 1, 1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Saturno_texture)
    drawTexturedSphere(Saturno_texture, 20.0, 20, 20)  # Radio de Saturno.
    glPopMatrix()

    # Dibujar el anillo de Saturno.
    glColor3f(0.7, 0.7, 0.7)  # Color gris claro para el anillo.
    glPushMatrix()
    glTranslatef(450.0 * math.cos(math.radians(angle_Saturno)), 0.0, -450.0 * math.sin(math.radians(angle_Saturno)))  # Posición del anillo (igual que la posición de Saturno).
    glRotatef(1000, 1, 1, 0)  # Rotar el anillo para que sea horizontal.
    glutSolidTorus(1.0, 40, 30, 30)  # Radio interior, radio exterior, segmentos radiales, segmentos anulares.
    glPopMatrix()

    # Luna 1 de Saturno (Titán).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(480.0 * math.cos(math.radians(angle_Saturno)), 0.0, -480.0 * math.sin(math.radians(angle_Saturno)))  # Orbitar alrededor del sol.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Titan)  # Textura de la Luna.
    drawTexturedSphere(Titan, 5.0, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Luna 2 de Saturno (Rea).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(500.0 * math.cos(math.radians(angle_Saturno)), 0.0, -500.0 * math.sin(math.radians(angle_Saturno)))  # Orbitar alrededor del sol.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Rea)  # Textura de la Luna.
    drawTexturedSphere(Rea, 3.5, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Luna 3 de Saturno (Dione).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(420.0 * math.cos(math.radians(angle_Saturno)), 0.0, -420.0 * math.sin(math.radians(angle_Saturno)))  # Orbitar alrededor del sol.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Dione)  # Textura de la Luna.
    drawTexturedSphere(Dione, 2.5, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Luna 4 de Saturno (Iapetus).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(400.0 * math.cos(math.radians(angle_Saturno)), 0.0, -400.0 * math.sin(math.radians(angle_Saturno)))  # Orbitar alrededor del sol.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Iapetus)  # Textura de la Luna.
    drawTexturedSphere(Iapetus, 3.0, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Urano.
    glColor3f(102, 204, 255)  # Color Azulado.
    glPushMatrix()
    glTranslatef(500.0 * math.cos(math.radians(angle_Urano)), 0.0, -500.0 * math.sin(math.radians(angle_Urano)))  # Orbitar alrededor del sol.
    glRotatef(angle_Jupiter, 1, 0, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Urano_texture)
    drawTexturedSphere(Urano_texture, 17.0, 20, 20)  # Radio de Saturno.
    glPopMatrix()

    # Dibujar el anillo de Urano.
    glColor3f(0, 51, 102)  # Color Azulado.
    glPushMatrix()
    glTranslatef(500.0 * math.cos(math.radians(angle_Urano)), 0.0, -500.0 * math.sin(math.radians(angle_Urano)))  # Posición del anillo (igual que la posición de Urano).
    glRotatef(1000, 0, 1, 0)  # Rotar el anillo para que sea horizontal.
    glutSolidTorus(0.5, 35, 30, 30)  # Radio interior, radio exterior, segmentos radiales, segmentos anulares.
    glPopMatrix()

    # Luna 1 de Urano (Titania).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(500.0 * math.cos(math.radians(angle_Urano)) + 30.0 * math.cos(math.radians(angle_luna)), 0.0, -500.0 * math.sin(math.radians(angle_Urano)) - 30.0 * math.sin(math.radians(angle_luna)))  # Orbitar alrededor de Urano.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Titania)  # Textura de la Luna.
    drawTexturedSphere(Titania, 4.0, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Luna 2 de Urano (Oberón).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(500.0 * math.cos(math.radians(angle_Urano)) - 40.0 * math.cos(math.radians(angle_luna)), 0.0, -500.0 * math.sin(math.radians(angle_Urano)) + 40.0 * math.sin(math.radians(angle_luna)))  # Orbitar alrededor de Urano.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Oberon)  # Textura de la Luna.
    drawTexturedSphere(Oberon, 3.5, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()   

    # Neptuno.
    glColor3f(0, 51, 102)  # Color Azulado.
    glPushMatrix()
    glTranslatef(550.0 * math.cos(math.radians(angle_neptuno)), 0.0, -550.0 * math.sin(math.radians(angle_neptuno)))  # Orbitar alrededor del sol.
    glRotatef(angle_Jupiter, 1, 1, 0)  # Rotar sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Neptuno_texture)
    drawTexturedSphere(Neptuno_texture, 15.0, 20, 20)  # Radio de Saturno.
    glPopMatrix()

    # Luna 1 de Neptuno (Tritón).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(550.0 * math.cos(math.radians(angle_neptuno)) - 30.0 * math.cos(math.radians(angle_luna)), 0.0, -550.0 * math.sin(math.radians(angle_neptuno)) + 30.0 * math.sin(math.radians(angle_luna)))  # Orbitar alrededor de Neptuno.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Triton)  # Textura de la Luna.
    drawTexturedSphere(Triton, 3.5, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

    # Luna 2 de Neptuno (Proteo).
    glColor3f(0.8, 0.8, 0.8)  # Color gris claro.
    glPushMatrix()
    glTranslatef(550.0 * math.cos(math.radians(angle_neptuno)) + 40.0 * math.cos(math.radians(angle_luna)), 0.0, -550.0 * math.sin(math.radians(angle_neptuno)) - 40.0 * math.sin(math.radians(angle_luna)))  # Orbitar alrededor de Neptuno.
    glRotatef(angle_luna, 0, 1, 0)  # Rotación sobre su propio eje.
    glBindTexture(GL_TEXTURE_2D, Proteo)  # Textura de la Luna.
    drawTexturedSphere(Proteo, 3.0, 20, 20)  # Tamaño de la Luna.
    glPopMatrix()

# Función de renderizado.
def renderScene():
    global angle_ast, angle_sun, angle_mercury, angle_venus, angle_earth, angle_mars, angle_Jupiter, angle_Saturno, angle_Urano, angle_neptuno, zoom, angle_luna

    # Incrementar los ángulos de rotación para cada planeta.
    angle_sun += 0.002
    angle_mercury += 0.004
    angle_venus += 0.002
    angle_earth += 0.01
    angle_luna += 0.1
    angle_mars += 0.04
    angle_Jupiter += 0.03
    angle_Saturno += 0.06
    angle_Urano += 0.009
    angle_neptuno += 0.006
    angle_ast += 0.02

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, zoom + 200.0, 600.0, 0.0, 0.0, -50.0, 0.0, 1.0, 0.0)

    drawOrbits()
    drawBackgroundSphere(700.0, 50, 50)  # Radio grande para cubrir el sistema solar.

    # Renderizar los planetas y órbitas.
    drawPlanets()

    glutSwapBuffers()
    glutPostRedisplay()  # Redibujar la ventana continuamente.

# Función principal
def main():
    global Fobos, Deimos, As_texture, background_texture, sun_texture, mercury_texture, venus_texture, earth_texture, mars_texture, Jupiter_texture, Saturno_texture, Urano_texture, Neptuno_texture, Luna_texture
    global angle_ast, angle_sun, angle_mercury, angle_venus, angle_earth, angle_mars, angle_Jupiter, angle_Saturno, angle_Urano, angle_neptuno, angle_luna
    global Io, Ganimedes, Calisto, Europa, Titan, Rea, Dione, Iapetus, Titania, Oberon, Triton, Proteo

    angle_sun = 0
    angle_mercury = 0
    angle_venus = 0
    angle_earth = 0
    angle_mars = 0
    angle_Jupiter = 0
    angle_Saturno = 0
    angle_Urano = 0
    angle_neptuno = 0
    angle_luna = 0
    angle_ast = 0

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(2500, 1000)  # Tamaño de la ventana.
    glutCreateWindow(b"Sistema Solar")
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    set_projection(2500, 1000)

    # Cargar las texturas.
    sun_texture = loadTexture("../Imagenes/Sistema_Solar/sol.jpg")
    mercury_texture = loadTexture("../Imagenes/Sistema_Solar/mercurio.jpg")
    venus_texture = loadTexture("../Imagenes/Sistema_Solar/venus.jpg")
    earth_texture = loadTexture("../Imagenes/Sistema_Solar/tierra.jpg")
    mars_texture = loadTexture("../Imagenes/Sistema_Solar/Marte.jpg")
    Jupiter_texture = loadTexture("../Imagenes/Sistema_Solar/Jupiter.png")
    Saturno_texture = loadTexture("../Imagenes/Sistema_Solar/Saturno.jpeg")
    Urano_texture = loadTexture("../Imagenes/Sistema_Solar/Urano.jpeg")
    Neptuno_texture = loadTexture("../Imagenes/Sistema_Solar/Neptuno.jpeg")
    Luna_texture = loadTexture("../Imagenes/Sistema_Solar/Luna.jpeg")
    As_texture = loadTexture("../Imagenes/Sistema_Solar/Asteoride.jpg")
    background_texture = loadTexture("../Imagenes/Sistema_Solar/Espacio.jpg")  # Reemplaza con la ruta de tu imagen de fondo.
    Fobos = loadTexture("../Imagenes/Sistema_Solar/LunaFobos.jpg")
    Deimos = loadTexture("../Imagenes/Sistema_Solar/LunaDeimos.jpg")
    Io = loadTexture("../Imagenes/Sistema_Solar/Io.jpg")
    Europa = loadTexture("../Imagenes/Sistema_Solar/Europa.jpg")
    Ganimedes = loadTexture("../Imagenes/Sistema_Solar/Ganimedes.jpeg")
    Calisto = loadTexture("../Imagenes/Sistema_Solar/Calisto.jpeg")
    Titan = loadTexture("../Imagenes/Sistema_Solar/Titan.jpg")
    Rea = loadTexture("../Imagenes/Sistema_Solar/Rea.jpg")
    Dione = loadTexture("../Imagenes/Sistema_Solar/Dione.jpeg")
    Iapetus = loadTexture("../Imagenes/Sistema_Solar/Iapetus.jpg")
    Titania = loadTexture("../Imagenes/Sistema_Solar/Titania.jpg")
    Oberon = loadTexture("../Imagenes/Sistema_Solar/Oberon.jpeg")
    Triton = loadTexture("../Imagenes/Sistema_Solar/Triton.jpeg")
    Proteo = loadTexture("../Imagenes/Sistema_Solar/Proteus.jpeg")

    glutSpecialFunc(specialKeys)
    glutDisplayFunc(renderScene)
    glutMainLoop()

if __name__ == "__main__":
    main()