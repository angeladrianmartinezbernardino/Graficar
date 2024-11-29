import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygltflib import GLTF2
import numpy as np
import math

def get_accessor_data(gltf, accessor_idx):
    """
    Extracts data from a GLTF accessor.
    """
    accessor = gltf.accessors[accessor_idx]
    buffer_view = gltf.bufferViews[accessor.bufferView]
    buffer_data = gltf.binary_blob()

    accessor_byte_offset = accessor.byteOffset or 0
    buffer_view_byte_offset = buffer_view.byteOffset or 0
    total_offset = buffer_view_byte_offset + accessor_byte_offset

    # Map component type to numpy dtype
    data_type = {
        5120: np.int8,
        5121: np.uint8,
        5122: np.int16,
        5123: np.uint16,
        5125: np.uint32,
        5126: np.float32
    }[accessor.componentType]

    # Determine number of components per element
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
    """
    Creates a translation matrix.
    """
    T = np.identity(4, dtype=np.float32)
    T[:3, 3] = translation
    return T

def scale_matrix(scale):
    """
    Creates a scaling matrix.
    """
    S = np.identity(4, dtype=np.float32)
    S[0, 0] = scale[0]
    S[1, 1] = scale[1]
    S[2, 2] = scale[2]
    return S

def quaternion_to_matrix(q):
    """
    Converts a quaternion into a rotation matrix.
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

def quaternion_from_euler(x, y, z):
    """
    Converts Euler angles (in radians) to a quaternion.
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

def quaternion_multiply(q1, q2):
    """
    Multiplies two quaternions.
    """
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2

    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2

    return [x, y, z, w]

def normalize_quaternion(q):
    """
    Normalizes a quaternion.
    """
    x, y, z, w = q
    norm = math.sqrt(x*x + y*y + z*z + w*w)
    if norm > 0:
        return [x / norm, y / norm, z / norm, w / norm]
    else:
        return [0, 0, 0, 1]

def compute_node_matrix(gltf, node_idx, matrices_cache):
    """
    Recursively computes the global transformation matrix of a node.
    """
    if node_idx in matrices_cache:
        return matrices_cache[node_idx]

    node = gltf.nodes[node_idx]

    # Start with the identity matrix.
    T = np.identity(4, dtype=np.float32)

    # If node.matrix is set, it overrides other transformations.
    if node.matrix is not None and any(node.matrix):
        T = np.array(node.matrix, dtype=np.float32).reshape(4, 4).T
    else:
        # Apply translation, rotation, and scale transformations.
        if node.translation is not None:
            T = np.dot(T, translate_matrix(node.translation))
        if node.rotation is not None:
            T = np.dot(T, quaternion_to_matrix(node.rotation))
        if node.scale is not None:
            T = np.dot(T, scale_matrix(node.scale))

    # If the node has a parent, multiply by the parent's matrix.
    parent_matrix = np.identity(4, dtype=np.float32)
    for idx, potential_parent in enumerate(gltf.nodes):
        if node_idx in (potential_parent.children or []):
            parent_matrix = compute_node_matrix(gltf, idx, matrices_cache)
            break
    T = np.dot(parent_matrix, T)
    matrices_cache[node_idx] = T
    return T

def draw_mesh_with_skinning(gltf, mesh_idx, joint_matrices):
    """
    Draws a mesh, applying skinning transformations.
    """
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

        # Check for skinning data.
        if primitive.attributes.JOINTS_0 is not None and primitive.attributes.WEIGHTS_0 is not None:
            # Get joint indices and weights.
            joints_accessor_idx = primitive.attributes.JOINTS_0
            joints = get_accessor_data(gltf, joints_accessor_idx)

            weights_accessor_idx = primitive.attributes.WEIGHTS_0
            weights = get_accessor_data(gltf, weights_accessor_idx)

            # Apply skinning.
            transformed_positions = np.zeros_like(positions)
            for i in range(len(positions)):
                pos = np.append(positions[i], 1.0)
                skin_matrix = np.zeros((4, 4), dtype=np.float32)
                for j in range(4):  # Up to 4 joints per vertex.
                    joint_idx_in_skin = joints[i][j]
                    weight = weights[i][j]
                    if weight > 0:
                        joint_matrix = joint_matrices[joint_idx_in_skin]
                        skin_matrix += weight * joint_matrix
                transformed_pos = np.dot(skin_matrix, pos)
                transformed_positions[i] = transformed_pos[:3]
        else:
            # No skinning; use positions as-is.
            transformed_positions = positions

        # Create buffers
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, transformed_positions.nbytes, transformed_positions, GL_STATIC_DRAW)

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

def render_node(gltf, node_idx, parent_matrix, joint_matrices):
    """
    Recursively renders a node and its children, applying transformations.
    """
    node = gltf.nodes[node_idx]

    # Compute the node's local transformation matrix.
    if node.matrix is not None and any(node.matrix):
        T = np.array(node.matrix, dtype=np.float32).reshape(4, 4).T
    else:
        T = np.identity(4, dtype=np.float32)
        if node.translation is not None:
            T = np.dot(T, translate_matrix(node.translation))
        if node.rotation is not None:
            T = np.dot(T, quaternion_to_matrix(node.rotation))
        if node.scale is not None:
            T = np.dot(T, scale_matrix(node.scale))

    # Combine with the parent's transformation matrix.
    T = np.dot(parent_matrix, T)

    if node.mesh is not None:
        glPushMatrix()
        glMultMatrixf(T.T)  # Transpose the matrix for OpenGL's column-major order
        if gltf.skins and node.skin is not None:
            # Apply skinning
            draw_mesh_with_skinning(gltf, node.mesh, joint_matrices)
        else:
            # Draw mesh without skinning
            draw_mesh(gltf, node.mesh)
        glPopMatrix()

    # Render the child nodes.
    if node.children:
        for child_idx in node.children:
            render_node(gltf, child_idx, T, joint_matrices)

def draw_mesh(gltf, mesh_idx):
    """
    Draws a mesh without skinning.
    """
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

def main():
    # Initialize Pygame and set up the OpenGL context.
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

    # Set up the projection matrix.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Animation variables.
    max_angle_arm = math.radians(45)  # Movement range in degrees for arms.
    max_angle_leg = math.radians(30)  # Movement range in degrees for legs.

    # Get the indices of the nodes corresponding to the arms and legs.
    left_arm_node_idx = 10   # 'Left_ShoulderJoint'
    right_arm_node_idx = 6   # 'Right_ShoulderJoint'
    left_leg_node_idx = 17   # 'Left_Hip'
    right_leg_node_idx = 21  # 'Right_Hip'

    # Nodes to animate.
    nodes_to_animate = [left_arm_node_idx, right_arm_node_idx, left_leg_node_idx, right_leg_node_idx]

    # Store initial rotations.
    initial_node_rotations = {}
    for node_idx in nodes_to_animate:
        node = gltf.nodes[node_idx]
        if node.rotation is None or len(node.rotation) == 0:
            node.rotation = [0, 0, 0, 1]  # Initialize rotation as a quaternion.
        initial_node_rotations[node_idx] = node.rotation

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
        time_sec = pygame.time.get_ticks() * 0.001
        angle_arm = math.sin(time_sec) * max_angle_arm
        angle_leg = math.sin(time_sec) * max_angle_leg

        # Animate arms (rotating around the Y-axis).
        left_arm_rotation = quaternion_from_euler(0, angle_arm, 0)
        right_arm_rotation = quaternion_from_euler(0, -angle_arm, 0)
        # Combine with initial rotations.
        combined_left_arm_rotation = quaternion_multiply(initial_node_rotations[left_arm_node_idx], left_arm_rotation)
        combined_left_arm_rotation = normalize_quaternion(combined_left_arm_rotation)
        combined_right_arm_rotation = quaternion_multiply(initial_node_rotations[right_arm_node_idx], right_arm_rotation)
        combined_right_arm_rotation = normalize_quaternion(combined_right_arm_rotation)
        gltf.nodes[left_arm_node_idx].rotation = combined_left_arm_rotation
        gltf.nodes[right_arm_node_idx].rotation = combined_right_arm_rotation

        # Animate legs (rotating around the Y-axis).
        left_leg_rotation = quaternion_from_euler(0, angle_leg, 0)
        right_leg_rotation = quaternion_from_euler(0, -angle_leg, 0)
        # Combine with initial rotations.
        combined_left_leg_rotation = quaternion_multiply(initial_node_rotations[left_leg_node_idx], left_leg_rotation)
        combined_left_leg_rotation = normalize_quaternion(combined_left_leg_rotation)
        combined_right_leg_rotation = quaternion_multiply(initial_node_rotations[right_leg_node_idx], right_leg_rotation)
        combined_right_leg_rotation = normalize_quaternion(combined_right_leg_rotation)
        gltf.nodes[left_leg_node_idx].rotation = combined_left_leg_rotation
        gltf.nodes[right_leg_node_idx].rotation = combined_right_leg_rotation

        # Compute joint matrices for skinning.
        joint_matrices = []
        if gltf.skins:
            skin = gltf.skins[0]  # Assuming there's at least one skin.
            inverse_bind_matrices = get_accessor_data(gltf, skin.inverseBindMatrices)
            matrices_cache = {}
            for i, joint_idx in enumerate(skin.joints):
                # Compute the joint's global transformation matrix.
                joint_matrix = compute_node_matrix(gltf, joint_idx, matrices_cache)
                # Multiply by the inverse bind matrix.
                inverse_bind_matrix = inverse_bind_matrices[i].reshape(4, 4).T
                joint_matrix = np.dot(joint_matrix, inverse_bind_matrix)
                joint_matrices.append(joint_matrix)

        # Draw the model.
        scene = gltf.scenes[gltf.scene]
        for node_idx in scene.nodes:
            render_node(gltf, node_idx, np.identity(4, dtype=np.float32), joint_matrices)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
