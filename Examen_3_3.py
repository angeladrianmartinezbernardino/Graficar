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

    # Calcular desplazamientos y tamaños
    accessor_byte_offset = accessor.byteOffset or 0
    buffer_view_byte_offset = buffer_view.byteOffset or 0
    total_offset = buffer_view_byte_offset + accessor_byte_offset
    data_type = {
        5120: np.byte,        # BYTE
        5121: np.ubyte,       # UNSIGNED_BYTE
        5122: np.short,       # SHORT
        5123: np.ushort,      # UNSIGNED_SHORT
        5125: np.uint32,      # UNSIGNED_INT
        5126: np.float32      # FLOAT
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
    # Inicializar Pygame y OpenGL
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)

    # Cargar el archivo GLB
    gltf = GLTF2().load('Robo Character Creation Project.glb')  # Reemplaza 'modelo.glb' con tu archivo

    # Asumimos que el modelo tiene una sola malla y un solo primitivo
    mesh = gltf.meshes[0]
    primitive = mesh.primitives[0]

    # Obtener datos de vértices
    position_accessor_idx = primitive.attributes.POSITION
    positions = get_accessor_data(gltf, position_accessor_idx).astype(np.float32)

    # Obtener datos de índices (si existen)
    if primitive.indices is not None:
        indices = get_accessor_data(gltf, primitive.indices).flatten().astype(np.uint32)
    else:
        indices = np.arange(len(positions), dtype=np.uint32)

    # Crear buffers de OpenGL
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Configurar punteros de vértices
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, None)

    # Configurar la proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Bucle principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Configurar vista
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        # Rotar el modelo para visualizarlo mejor
        glRotatef(pygame.time.get_ticks() * 0.05, 0, 1, 0)

        # Dibujar el modelo
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
