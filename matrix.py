import math
from numpy import array, dot, zeros, float32

def translate(matrix, x=0.0, y=0.0, z=0.0):
	"""
	Translate (move) a matrix in the x, y and z axes.

	:param matrix: Matrix to translate.
	:param x: direction and magnitude to translate in x axis. Defaults to 0.
	:param y: direction and magnitude to translate in y axis. Defaults to 0.
	:param z: direction and magnitude to translate in z axis. Defaults to 0.
	:return: The translated matrix.
	"""
	translation_matrix = array([
		[1.0, 0.0, 0.0, x],
		[0.0, 1.0, 0.0, y],
		[0.0, 0.0, 1.0, z],
		[0.0, 0.0, 0.0, 1.0], ],
		dtype=matrix.dtype, ).T
	matrix[...] = dot(matrix, translation_matrix)
	return matrix


def frustum(left, right, bottom, top, znear, zfar):
	"""
	Build a perspective matrix from the clipping planes, or camera 'frustrum'
	volume.

	:param left: left position of the near clipping plane.
	:param right: right position of the near clipping plane.
	:param bottom: bottom position of the near clipping plane.
	:param top: top position of the near clipping plane.
	:param znear: z depth of the near clipping plane.
	:param zfar: z depth of the far clipping plane.

	:return: A perspective matrix.
	"""
	perspective_matrix = zeros((4, 4), dtype=float32)
	perspective_matrix[0, 0] = +2.0 * znear / (right - left)
	perspective_matrix[2, 0] = (right + left) / (right - left)
	perspective_matrix[1, 1] = +2.0 * znear / (top - bottom)
	perspective_matrix[3, 1] = (top + bottom) / (top - bottom)
	perspective_matrix[2, 2] = -(zfar + znear) / (zfar - znear)
	perspective_matrix[3, 2] = -2.0 * znear * zfar / (zfar - znear)
	perspective_matrix[2, 3] = -1.0
	return perspective_matrix


def perspective(fovy, aspect, znear, zfar):
	"""
	Build a perspective matrix from field of view, aspect ratio and depth
	planes.

	:param fovy: the field of view angle in the y axis.
	:param aspect: aspect ratio of our view port.
	:param znear: z depth of the near clipping plane.
	:param zfar: z depth of the far clipping plane.

	:return: A perspective matrix.
	"""
	h = math.tan(fovy / 360.0 * math.pi) * znear
	w = h * aspect
	return frustum(-w, w, -h, h, znear, zfar)


def rotate(matrix, angle, x, y, z):
	"""
	Rotate a matrix around an axis.

	:param matrix: The matrix to rotate.
	:param angle: The angle to rotate by.
	:param x: x of axis to rotate around.
	:param y: y of axis to rotate around.
	:param z: z of axis to rotate around.

	:return: The rotated matrix
	"""
	angle = math.pi * angle / 180
	c, s = math.cos(angle), math.sin(angle)
	n = math.sqrt(x * x + y * y + z * z)
	x, y, z = x / n, y / n, z / n
	cx, cy, cz = (1 - c) * x, (1 - c) * y, (1 - c) * z
	rotation_matrix = array([
		[cx * x + c, cy * x - z * s, cz * x + y * s, 0],
		[cx * y + z * s, cy * y + c, cz * y - x * s, 0],
		[cx * z - y * s, cy * z + x * s, cz * z + c, 0],
		[0, 0, 0, 1], ], dtype=matrix.dtype, ).T
	matrix[...] = dot(matrix, rotation_matrix)
	return matrix


class Rotation:
	"""
	Data class that stores rotation angles in three axes.
	"""

	def __init__(self):
		self.theta = 20
		self.phi = 40
		self.psi = 25
