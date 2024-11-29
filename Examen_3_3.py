import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygltflib import GLTF2
import numpy as np
import math

def get_accessor_data(gltf, accessor_idx):
    accessor = gltf.accessors[accessor_idx]
    buffer_view = gltf.bufferViews[accessor.bufferView]
    buffer_data = gltf.binary_blob()

    accessor_byte_offset = accessor.byteOffset or 0
    buffer_view_byte_offset = buffer_view.byteOffset or 0
    total_offset = buffer_view_byte_offset + accessor_byte_offset

    data_type = {
        5120: np.int8,
        5121: np.uint8,
        5122: np.int16,
        5123: np.uint16,
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

def translate_matrix(translation):
    T = np.identity(4, dtype=np.float32)
    T[:3, 3] = translation  # Corrected translation placement
    return T

def scale_matrix(scale):
    S = np.identity(4, dtype=np.float32)
    S[0, 0] = scale[0]
    S[1, 1] = scale[1]
    S[2, 2] = scale[2]
    return S

def quaternion_to_matrix(q):
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

def quaternion_from_euler(x, y, z):
    # Convert Euler angles (in radians) to quaternion.
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

def draw_mesh(gltf, mesh_idx):
    mesh = gltf.meshes[mesh_idx]
    for primitive in mesh.primitives:
        # Get vertex data.
        position_accessor_idx = primitive.attributes.POSITION
        positions = get_accessor_data(gltf, position_accessor_idx).astype(np.float32)

        # Get indices.
        if primitive.indices is not None:
            indices = get_accessor_data(gltf, primitive.indices).flatten().astype(np.uint32)
        else:
            indices = np.arange(len(positions), dtype=np.uint32)

        # Create buffers
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_STATIC_DRAW)

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

def render_node(gltf, node_idx, parent_matrix=np.identity(4, dtype=np.float32)):
    node = gltf.nodes[node_idx]

    # Get the node's transformation matrix.
    T = np.identity(4, dtype=np.float32)
    if node.matrix is not None and any(node.matrix):
        T = np.array(node.matrix, dtype=np.float32).reshape(4, 4).T
    else:
        if node.translation is not None and any(node.translation):
            T = np.dot(T, translate_matrix(node.translation))
        if node.rotation is not None and any(node.rotation):
            T = np.dot(T, quaternion_to_matrix(node.rotation))
        if node.scale is not None and any(node.scale):
            T = np.dot(T, scale_matrix(node.scale))

    # Combine with the parent's transformation matrix.
    T = np.dot(parent_matrix, T)

    # If the node has a mesh, draw it.
    if node.mesh is not None:
        glPushMatrix()
        glMultMatrixf(T.T)  # Transpose the matrix for OpenGL's column-major order
        draw_mesh(gltf, node.mesh)
        glPopMatrix()

    # Render the child nodes.
    if node.children:
        for child_idx in node.children:
            render_node(gltf, child_idx, T)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)

    # Load the GLB model.
    gltf = GLTF2().load('Robot.glb')

    # Print node information to identify correct node indices.
    for idx, node in enumerate(gltf.nodes):
        print(f"Node {idx}: Name='{node.name}', Children={node.children}, Mesh={node.mesh}")

    # Projection.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Animation variables.
    max_angle = 0.5  # Movement range in radians.

    # Get the indices of the nodes corresponding to the arms and legs.
    # Use the node indices from the printed information.
    left_arm_node_idx = 10   # 'Left_ShoulderJoint'
    right_arm_node_idx = 6   # 'Right_ShoulderJoint'
    left_leg_node_idx = 17   # 'Left_Hip'
    right_leg_node_idx = 21  # 'Right_Hip'

    # Ensure the nodes have rotation initialized.
    nodes_to_animate = [left_arm_node_idx, right_arm_node_idx, left_leg_node_idx, right_leg_node_idx]
    for node_idx in nodes_to_animate:
        node = gltf.nodes[node_idx]
        if node.rotation is None or len(node.rotation) == 0:
            node.rotation = [0, 0, 0, 1]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Clear the screen.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set up the camera.
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 1, 10, 0, 0, 0, 0, 1, 0)

        # Apply animation.
        time = pygame.time.get_ticks() * 0.001
        angle = math.sin(time) * max_angle

        # Animate arms.
        arm_rotation = quaternion_from_euler(angle, 0, 0)
        gltf.nodes[left_arm_node_idx].rotation = arm_rotation
        gltf.nodes[right_arm_node_idx].rotation = arm_rotation

        # Animate legs.
        leg_rotation = quaternion_from_euler(-angle, 0, 0)
        gltf.nodes[left_leg_node_idx].rotation = leg_rotation
        gltf.nodes[right_leg_node_idx].rotation = leg_rotation

        # Draw the model.
        scene = gltf.scenes[gltf.scene]
        for node_idx in scene.nodes:
            render_node(gltf, node_idx)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
