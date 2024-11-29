import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygltflib import GLTF2
import numpy as np
import math

def obtener_datos_accesor(gltf, indice_accesor):
    """
    Extrae datos de un accesor GLTF.
    """
    accesor = gltf.accessors[indice_accesor]
    vista_buffer = gltf.bufferViews[accesor.bufferView]
    datos_buffer = gltf.binary_blob()

    desplazamiento_byte_accesor = accesor.byteOffset or 0
    desplazamiento_byte_vista_buffer = vista_buffer.byteOffset or 0
    desplazamiento_total = desplazamiento_byte_vista_buffer + desplazamiento_byte_accesor

    # Mapea el tipo de componente a un tipo de datos de numpy.
    tipo_dato = {
        5120: np.int8,
        5121: np.uint8,
        5122: np.int16,
        5123: np.uint16,
        5125: np.uint32,
        5126: np.float32
    }[accesor.componentType]

    # Determina el número de componentes por elemento.
    conteo_tipo = {
        "SCALAR": 1,
        "VEC2": 2,
        "VEC3": 3,
        "VEC4": 4,
        "MAT2": 4,
        "MAT3": 9,
        "MAT4": 16
    }[accesor.type]

    longitud_datos = accesor.count * conteo_tipo
    datos = np.frombuffer(datos_buffer, dtype=tipo_dato, count=longitud_datos, offset=desplazamiento_total)
    return datos.reshape((accesor.count, conteo_tipo))

def matriz_traslacion(traslacion):
    """
    Crea una matriz de traslación.
    """
    T = np.identity(4, dtype=np.float32)
    T[:3, 3] = traslacion
    return T

def matriz_escala(escala):
    """
    Crea una matriz de escala.
    """
    S = np.identity(4, dtype=np.float32)
    S[0, 0] = escala[0]
    S[1, 1] = escala[1]
    S[2, 2] = escala[2]
    return S

def quaternion_a_matriz(q):
    """
    Convierte un cuaternión en una matriz de rotación.
    """
    x, y, z, w = q
    n = x*x + y*y + z*z + w*w
    s = 2.0 / n if n > 0.0 else 0.0

    wx, wy, wz = s * w * x, s * w * y, s * w * z
    xx, xy, xz = s * x * x, s * x * y, s * x * z
    yy, yz, zz = s * y * y, s * y * z, s * z * z

    M = np.identity(4, dtype=np.float32)
    M[0, 0] = 1.0 - (yy + zz)
    M[0, 1] = xy - wz
    M[0, 2] = xz + wy
    M[1, 0] = xy + wz
    M[1, 1] = 1.0 - (xx + zz)
    M[1, 2] = yz - wx
    M[2, 0] = xz - wy
    M[2, 1] = yz + wx
    M[2, 2] = 1.0 - (xx + yy)
    return M

def quaternion_desde_euler(x, y, z):
    """
    Convierte ángulos de Euler (en radianes) a un cuaternión.
    """
    cy = math.cos(z * 0.5)
    sy = math.sin(z * 0.5)
    cp = math.cos(y * 0.5)
    sp = math.sin(y * 0.5)
    cr = math.cos(x * 0.5)
    sr = math.sin(x * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy

    return [qx, qy, qz, qw]

def multiplicar_quaterniones(q1, q2):
    """
    Multiplica dos cuaterniones.
    """
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2

    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2

    return [x, y, z, w]

def normalizar_quaternion(q):
    """
    Normaliza un cuaternión.
    """
    x, y, z, w = q
    norma = math.sqrt(x*x + y*y + z*z + w*w)
    if norma > 0:
        return [x / norma, y / norma, z / norma, w / norma]
    else:
        return [0, 0, 0, 1]

def calcular_matriz_nodo(gltf, indice_nodo, cache_matrices):
    """
    Calcula recursivamente la matriz de transformación global de un nodo.
    """
    if indice_nodo in cache_matrices:
        return cache_matrices[indice_nodo]

    nodo = gltf.nodes[indice_nodo]

    # Comienza con la matriz identidad.
    T = np.identity(4, dtype=np.float32)

    # Si node.matrix está establecido, anula otras transformaciones.
    if nodo.matrix is not None and any(nodo.matrix):
        T = np.array(nodo.matrix, dtype=np.float32).reshape(4, 4).T
    else:
        # Aplica las transformaciones de traslación, rotación y escala.
        if nodo.translation is not None:
            T = np.dot(T, matriz_traslacion(nodo.translation))
        if nodo.rotation is not None:
            T = np.dot(T, quaternion_a_matriz(nodo.rotation))
        if nodo.scale is not None:
            T = np.dot(T, matriz_escala(nodo.scale))

    # Si el nodo tiene un padre, multiplica por la matriz del padre.
    matriz_padre = np.identity(4, dtype=np.float32)
    for idx, posible_padre in enumerate(gltf.nodes):
        if indice_nodo in (posible_padre.children or []):
            matriz_padre = calcular_matriz_nodo(gltf, idx, cache_matrices)
            break
    T = np.dot(matriz_padre, T)
    cache_matrices[indice_nodo] = T
    return T

def dibujar_malla_con_skinning(gltf, indice_malla, matrices_juntas):
    """
    Dibuja una malla, aplicando transformaciones de skinning.
    """
    malla = gltf.meshes[indice_malla]
    for primitiva in malla.primitives:
        # Obtiene datos de vértices.
        indice_accesor_posicion = primitiva.attributes.POSITION
        posiciones = obtener_datos_accesor(gltf, indice_accesor_posicion).astype(np.float32)

        # Obtiene índices.
        if primitiva.indices is not None:
            indices = obtener_datos_accesor(gltf, primitiva.indices).flatten().astype(np.uint32)
        else:
            indices = np.arange(len(posiciones), dtype=np.uint32)

        # Verifica si hay datos de skinning.
        if primitiva.attributes.JOINTS_0 is not None and primitiva.attributes.WEIGHTS_0 is not None:
            # Obtiene índices de las juntas y pesos.
            indice_accesor_juntas = primitiva.attributes.JOINTS_0
            juntas = obtener_datos_accesor(gltf, indice_accesor_juntas)

            indice_accesor_pesos = primitiva.attributes.WEIGHTS_0
            pesos = obtener_datos_accesor(gltf, indice_accesor_pesos)

            # Aplica skinning.
            posiciones_transformadas = np.zeros_like(posiciones)
            for i in range(len(posiciones)):
                pos = np.append(posiciones[i], 1.0)
                matriz_skin = np.zeros((4, 4), dtype=np.float32)
                for j in range(4):  # Hasta 4 juntas por vértice.
                    indice_junta_en_skin = juntas[i][j]
                    peso = pesos[i][j]
                    if peso > 0:
                        matriz_junta = matrices_juntas[indice_junta_en_skin]
                        matriz_skin += peso * matriz_junta
                pos_transformada = np.dot(matriz_skin, pos)
                posiciones_transformadas[i] = pos_transformada[:3]
        else:
            # Sin skinning; usa posiciones tal cual.
            posiciones_transformadas = posiciones

        # Crea buffers.
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, posiciones_transformadas.nbytes, posiciones_transformadas, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glDeleteBuffers(1, [VBO])
        glDeleteBuffers(1, [EBO])

def renderizar_nodo(gltf, indice_nodo, matriz_padre, matrices_juntas):
    """
    Renderiza recursivamente un nodo y sus hijos, aplicando transformaciones.
    """
    nodo = gltf.nodes[indice_nodo]

    # Calcula la matriz de transformación local del nodo.
    if nodo.matrix is not None and any(nodo.matrix):
        T = np.array(nodo.matrix, dtype=np.float32).reshape(4, 4).T
    else:
        T = np.identity(4, dtype=np.float32)
        if nodo.translation is not None:
            T = np.dot(T, matriz_traslacion(nodo.translation))
        if nodo.rotation is not None:
            T = np.dot(T, quaternion_a_matriz(nodo.rotation))
        if nodo.scale is not None:
            T = np.dot(T, matriz_escala(nodo.scale))

    # Combina con la matriz de transformación del padre.
    T = np.dot(matriz_padre, T)

    if nodo.mesh is not None:
        glPushMatrix()
        glMultMatrixf(T.T)  # Transpone la matriz para el orden de columnas de OpenGL.
        if gltf.skins and nodo.skin is not None:
            # Aplica skinning.
            dibujar_malla_con_skinning(gltf, nodo.mesh, matrices_juntas)
        else:
            # Dibuja la malla sin skinning.
            dibujar_malla(gltf, nodo.mesh)
        glPopMatrix()

    # Renderiza los nodos hijos.
    if nodo.children:
        for indice_hijo in nodo.children:
            renderizar_nodo(gltf, indice_hijo, T, matrices_juntas)

def dibujar_malla(gltf, indice_malla):
    """
    Dibuja una malla sin skinning.
    """
    malla = gltf.meshes[indice_malla]
    for primitiva in malla.primitives:
        # Obtiene datos de vértices.
        indice_accesor_posicion = primitiva.attributes.POSITION
        posiciones = obtener_datos_accesor(gltf, indice_accesor_posicion).astype(np.float32)

        # Obtiene índices.
        if primitiva.indices is not None:
            indices = obtener_datos_accesor(gltf, primitiva.indices).flatten().astype(np.uint32)
        else:
            indices = np.arange(len(posiciones), dtype=np.uint32)

        # Crea buffers.
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, posiciones.nbytes, posiciones, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        glDeleteBuffers(1, [VBO])
        glDeleteBuffers(1, [EBO])

def main():
    # Inicializa Pygame y configura el contexto de OpenGL.
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    reloj = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)

    # Carga el modelo GLB.
    gltf = GLTF2().load('Robot.glb')

    # Imprime información de los nodos para identificar los índices correctos.
    for idx, nodo in enumerate(gltf.nodes):
        print(f"Nodo {idx}: Nombre='{nodo.name}', Hijos={nodo.children}, Malla={nodo.mesh}")

    # Configura la matriz de proyección.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Variables de animación.
    angulo_max_brazo = math.radians(45)  # Rango de movimiento en grados para los brazos.
    angulo_max_pierna = math.radians(30)  # Rango de movimiento en grados para las piernas.

    # Obtiene los índices de los nodos correspondientes a los brazos y piernas.
    indice_nodo_brazo_izquierdo = 10   # 'Left_ShoulderJoint'
    indice_nodo_brazo_derecho = 6      # 'Right_ShoulderJoint'
    indice_nodo_pierna_izquierda = 17   # 'Left_Hip'
    indice_nodo_pierna_derecha = 21     # 'Right_Hip'

    # Nodos a animar.
    nodos_a_animar = [indice_nodo_brazo_izquierdo, indice_nodo_brazo_derecho, indice_nodo_pierna_izquierda, indice_nodo_pierna_derecha]

    # Almacena rotaciones iniciales.
    rotaciones_iniciales_nodos = {}
    for indice_nodo in nodos_a_animar:
        nodo = gltf.nodes[indice_nodo]
        if nodo.rotation is None or len(nodo.rotation) == 0:
            nodo.rotation = [0, 0, 0, 1]  # Inicializa la rotación como un cuaternión.
        rotaciones_iniciales_nodos[indice_nodo] = nodo.rotation

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Limpia la pantalla.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Configura la cámara.
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 1, 10, 0, 0, 0, 0, 1, 0)

        # Aplica la animación.
        tiempo_seg = pygame.time.get_ticks() * 0.001
        angulo_brazo = math.sin(tiempo_seg) * angulo_max_brazo
        angulo_pierna = math.sin(tiempo_seg) * angulo_max_pierna

        # Anima los brazos (rotando alrededor del eje Y).
        rotacion_brazo_izquierdo = quaternion_desde_euler(0, angulo_brazo, 0)
        rotacion_brazo_derecho = quaternion_desde_euler(0, -angulo_brazo, 0)
        # Combina con las rotaciones iniciales.
        rotacion_combinada_brazo_izquierdo = multiplicar_quaterniones(rotaciones_iniciales_nodos[indice_nodo_brazo_izquierdo], rotacion_brazo_izquierdo)
        rotacion_combinada_brazo_izquierdo = normalizar_quaternion(rotacion_combinada_brazo_izquierdo)
        rotacion_combinada_brazo_derecho = multiplicar_quaterniones(rotaciones_iniciales_nodos[indice_nodo_brazo_derecho], rotacion_brazo_derecho)
        rotacion_combinada_brazo_derecho = normalizar_quaternion(rotacion_combinada_brazo_derecho)
        gltf.nodes[indice_nodo_brazo_izquierdo].rotation = rotacion_combinada_brazo_izquierdo
        gltf.nodes[indice_nodo_brazo_derecho].rotation = rotacion_combinada_brazo_derecho

        # Anima las piernas (rotando alrededor del eje Y).
        rotacion_pierna_izquierda = quaternion_desde_euler(0, angulo_pierna, 0)
        rotacion_pierna_derecha = quaternion_desde_euler(0, -angulo_pierna, 0)
        # Combina con las rotaciones iniciales.
        rotacion_combinada_pierna_izquierda = multiplicar_quaterniones(rotaciones_iniciales_nodos[indice_nodo_pierna_izquierda], rotacion_pierna_izquierda)
        rotacion_combinada_pierna_izquierda = normalizar_quaternion(rotacion_combinada_pierna_izquierda)
        rotacion_combinada_pierna_derecha = multiplicar_quaterniones(rotaciones_iniciales_nodos[indice_nodo_pierna_derecha], rotacion_pierna_derecha)
        rotacion_combinada_pierna_derecha = normalizar_quaternion(rotacion_combinada_pierna_derecha)
        gltf.nodes[indice_nodo_pierna_izquierda].rotation = rotacion_combinada_pierna_izquierda
        gltf.nodes[indice_nodo_pierna_derecha].rotation = rotacion_combinada_pierna_derecha

        # Calcula matrices de las juntas para el skinning.
        matrices_juntas = []
        if gltf.skins:
            skin = gltf.skins[0]  # Asumiendo que hay al menos un skin.
            matrices_bind_inversas = obtener_datos_accesor(gltf, skin.inverseBindMatrices)
            cache_matrices = {}
            for i, indice_junta in enumerate(skin.joints):
                # Calcula la matriz de transformación global de la junta.
                matriz_junta = calcular_matriz_nodo(gltf, indice_junta, cache_matrices)
                # Multiplica por la matriz bind inversa.
                matriz_bind_inversa = matrices_bind_inversas[i].reshape(4, 4).T
                matriz_junta = np.dot(matriz_junta, matriz_bind_inversa)
                matrices_juntas.append(matriz_junta)

        # Dibuja el modelo.
        escena = gltf.scenes[gltf.scene]
        for indice_nodo in escena.nodes:
            renderizar_nodo(gltf, indice_nodo, np.identity(4, dtype=np.float32), matrices_juntas)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
