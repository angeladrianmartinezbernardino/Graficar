from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

# Código del shader de vértices.
vertex_shader_source = """
#version 330 core

layout(location = 0) in vec2 position;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

# Código del shader de fragmentos.
fragment_shader_source = """
#version 330 core

out vec4 color;

uniform vec2 u_resolution;
uniform vec2 u_center;
uniform float u_zoom;

void main()
{
    vec2 coord = (gl_FragCoord.xy - u_resolution * 0.5) / u_zoom + u_center;

    float x = 0.0;
    float y = 0.0;

    int max_iter = 100;
    int i;

    for(i = 0; i < max_iter; i++)
    {
        float x_new = x * x - y * y + coord.x;
        y = 2.0 * x * y + coord.y;
        x = x_new;

        if(x * x + y * y > 4.0)
            break;
    }

    float t = float(i) / float(max_iter);
    color = vec4(t, t, t, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    # Verificar el estado de compilación.
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not(result):
        error = glGetShaderInfoLog(shader).decode()
        print("Error al compilar el shader:\n", error)
        exit(1)

    return shader

def create_program(vertex_src, fragment_src):
    vertex_shader = compile_shader(vertex_src, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_src, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    # Verificar el estado de enlace.
    result = glGetProgramiv(program, GL_LINK_STATUS)
    if not(result):
        error = glGetProgramInfoLog(program).decode()
        print("Error al enlazar el programa:\n", error)
        exit(1)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)

    # Configurar los uniformes
    glUniform2f(glGetUniformLocation(shader_program, "u_resolution"), width, height)
    glUniform2f(glGetUniformLocation(shader_program, "u_center"), center_x, center_y)
    glUniform1f(glGetUniformLocation(shader_program, "u_zoom"), zoom)

    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glBindVertexArray(0)

    glutSwapBuffers()

def reshape(w, h):
    global width, height
    width = w
    height = h
    glViewport(0, 0, w, h)

def keyboard(key, x, y):
    global center_x, center_y, zoom

    if key == b'q' or key == b'\x1b':  # Tecla Escape
        glutLeaveMainLoop()
    elif key == b'+':
        zoom *= 1.1
    elif key == b'-':
        zoom /= 1.1
    elif key == b'w':
        center_y += 0.1 / zoom
    elif key == b's':
        center_y -= 0.1 / zoom
    elif key == b'a':
        center_x -= 0.1 / zoom
    elif key == b'd':
        center_x += 0.1 / zoom

    glutPostRedisplay()

if __name__ == "__main__":
    import sys

    # Parámetros iniciales.
    width, height = 800, 600
    center_x, center_y = -0.5, 0.0
    zoom = 300.0

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Fractal de Mandelbrot")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    # Compilar shaders y crear programa.
    shader_program = create_program(vertex_shader_source, fragment_shader_source)

    # Configurar datos de vértices (dos triángulos que cubren la pantalla).
    vertices = np.array([
        -1.0, -1.0,
         1.0, -1.0,
        -1.0,  1.0,
         1.0,  1.0
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    pos_attrib = glGetAttribLocation(shader_program, 'position')
    glEnableVertexAttribArray(pos_attrib)
    glVertexAttribPointer(pos_attrib, 2, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    glutMainLoop()
