import ctypes
import OpenGL.GL as GL

from numpy import array, float32#, eye, zeros, uint32


def _file_to_str(filename):
	with open(filename, 'r') as my_file:
		data = my_file.read()
	return data

def _create_shader(ver_file_name, frag_file_name):
	vertex_code = _file_to_str(ver_file_name)
	fragment_code = _file_to_str(frag_file_name)

	program = GL.glCreateProgram()
	vertex = GL.glCreateShader(GL.GL_VERTEX_SHADER)
	fragment = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
	GL.glShaderSource(vertex, vertex_code)
	GL.glCompileShader(vertex)

	# this logs issues the shader compiler finds.
	log = GL.glGetShaderInfoLog(vertex)
	if isinstance(log, bytes):
		log = log.decode()
		print(log)

	GL.glAttachShader(program, vertex)
	GL.glShaderSource(fragment, fragment_code)
	GL.glCompileShader(fragment)

	# this logs issues the shader compiler finds.
	log = GL.glGetShaderInfoLog(fragment)
	if isinstance(log, bytes):
		log = log.decode()
		print(log)

	GL.glAttachShader(program, fragment)
	GL.glValidateProgram(program)
	GL.glLinkProgram(program)

	log = GL.glGetProgramInfoLog(program)
	if isinstance(log, bytes):
		log = log.decode()
		print(log)

	GL.glDetachShader(program, vertex)
	GL.glDetachShader(program, fragment)
	return program

def _init_gl(ver_file_name, frag_file_name):
	vertices = array([
		-.5, -.5, 0, 0, 1,
		.5, -.5, 0, 1, 1,
		-.5, .5, 0, 0, 0,
		
		-.5, .5, 0, 0, 0,
		.5, .5, 0, 1, 0,
		.5, -.5, 0, 1, 1], dtype=float32)

	program = _create_shader(ver_file_name, frag_file_name)
	GL.glUseProgram(program)

	VAO = GL.glGenVertexArrays(1)
	GL.glBindVertexArray(VAO)

	VBO = GL.glGenBuffers(1)
	GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
	GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

	size = int(int(vertices.nbytes / 6) / 5)

	print("SSIZE=",size)

	stride = 5 * size
	offset1 = ctypes.c_void_p(0 * size)
	offset2 = ctypes.c_void_p(3 * size)

	loc = 0# GL.glGetAttribLocation(program, "v_position")
	GL.glEnableVertexAttribArray(loc)
	GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, stride, offset1)

	loc = 1# GL.glGetAttribLocation(program, "v_texCoord")
	GL.glEnableVertexAttribArray(loc)
	GL.glVertexAttribPointer(loc, 2, GL.GL_FLOAT, False, stride, offset2)

	GL.glBindVertexArray(0)
	return program, VAO, VBO


class Shader:

	def __init__(self, ver_file_name, frag_file_name):
		self.prog_id = _create_shader(ver_file_name, frag_file_name)
		self.vertex = 6

	def use(self):
		GL.glUseProgram(self.prog_id)

	#def __del__(self):
	#	GL.glDeleteProgram(self.prog_id)

	def draw(self):
		GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex)
		GL.glBindVertexArray(0)

	def uniform_matrix(self, name, matrix):
		loc = GL.glGetUniformLocation(self.prog_id, name)
		GL.glUniformMatrix4fv(loc, 1, False, matrix)
