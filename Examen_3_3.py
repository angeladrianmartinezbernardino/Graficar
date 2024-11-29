import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygltflib import GLTF2
import numpy as np

def get_accessor_data(gltf, accessor_idx):
    accessor = gltf.accessors[accessor_idx]
    buffer_view = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[buffer_view.buffer]
    buffer_data = gltf.binary_blob()

    accessor_byte_offset = accessor.byteOffset or 0
    buffer_view_byte_offset = buffer_view.byteOffset or 0
    total_offset = buffer_view_byte_offset + accessor_byte_offset

    data_type = {
        5120: np.byte,
        5121: np.ubyte,
        5122: np.short,
        5123: np.ushort,
        5125: np.uint32,
        5126: np.float32
    }[accessor.componentType]

    type_count = {
        "SCALAR": 1,
        "VEC2": 2,
        "VEC3": 3,
        "VEC4": 4,
        "MAT2": 4,
        "MAT3": 9,
        "MAT4": 16
    }[accessor.type]

    data_length = accessor.count * type_count
    data = np.frombuffer(buffer_data, dtype=data_type, count=data_length, offset=total_offset)
    return data.reshape((accessor.count, type_count))

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)

    # Cargar el modelo GLB
    gltf = GLTF2().load('Robo Character Creation Project.glb')

    mesh = gltf.meshes[0]
    primitive = mesh.primitives[0]

    # Obtener datos de vértices
    position_accessor_idx = primitive.attributes.POSITION
    positions = get_accessor_data(gltf, position_accessor_idx).astype(np.float32)

    # Obtener índices
    if primitive.indices is not None:
        indices = get_accessor_data(gltf, primitive.indices).flatten().astype(np.uint32)
    else:
        indices = np.arange(len(positions), dtype=np.uint32)

    # Crear buffers
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, None)

    # Proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Variables para animación
    running_angle = 0
    direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Configurar cámara
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 1, 10, 0, 0, 0, 0, 1, 0)

        # Aplicar animación
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glRotatef(running_angle, 0, 1, 0)  # Rotar para simular movimiento
        running_angle += direction * 5  # Velocidad de animación
        if running_angle > 20 or running_angle < -20:
            direction *= -1  # Cambiar dirección

        # Dibujar modelo
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
