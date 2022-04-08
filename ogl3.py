import ctypes

import OpenGL.GL as GL

from matrix import translate, perspective, rotate, Rotation

from numpy import array, eye, zeros, float32, uint32


def _file_to_str(filename):
	with open(filename, 'r') as my_file:
		data = my_file.read()
	return data

def _create_shader(vShader_file_name, fShader_file_name):
	vertex_code = _file_to_str(vShader_file_name)
	fragment_code = _file_to_str(fShader_file_name)

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

def init_gl2():
	vertices = array([
		-.5, -.5, 0, 0, 1,
		.5, -.5, 0, 1, 1,
		-.5, .5, 0, 0, 0,
		
		-.5, .5, 0, 0, 0,
		.5, .5, 0, 1, 0,
		.5, -.5, 0, 1, 1], dtype=float32)

	program = _create_shader("res/shaders/sh2.vert","res/shaders/sh2.frag")
	GL.glUseProgram(program)

	VAO = GL.glGenVertexArrays(1)
	GL.glBindVertexArray(VAO)

	VBO = GL.glGenBuffers(1)
	GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
	GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_DYNAMIC_DRAW)

	size = int(int(vertices.nbytes / 6) / 5)
	stride = 5 * size
	offset1 = ctypes.c_void_p(0 * size)
	offset2 = ctypes.c_void_p(3 * size)

	loc = GL.glGetAttribLocation(program, "v_position")
	GL.glEnableVertexAttribArray(loc)
	GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, stride, offset1)

	loc = GL.glGetAttribLocation(program, "v_texCoord")
	GL.glEnableVertexAttribArray(loc)
	GL.glVertexAttribPointer(loc, 2, GL.GL_FLOAT, False, stride, offset2)

	GL.glBindVertexArray(0)
	return VAO, VBO

def shader_bind(p):
	VAO, _ = p
	GL.glBindVertexArray(VAO)

def draw_2():
	GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
	GL.glBindVertexArray(0)

def init_gl(display_size):
	# Create shaders
	# --------------------------------------
	program = _create_shader("res/shaders/sh1.glslv","res/shaders/sh1.glslf")
	GL.glUseProgram(program)

	# Create vertex buffers and shader constants
	# ------------------------------------------

	# Cube Data
	vertices = zeros(
		8, [("vertex_position", float32, 3), ("vertex_colour", float32, 4)]
	)

	vertices["vertex_position"] = [
		[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
		[1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1], ]

	vertices["vertex_colour"] = [
		[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
		[1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1], ]

	filled_cube_indices = array(
		[0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 1, 1, 6, 7, 1, 7, 2, 7, 4, 3, 7, 3, 2, 4, 7, 6, 4, 6, 5, ],
		dtype=uint32, )

	outline_cube_indices = array(
		[0, 1, 1, 2, 2, 3, 3, 0, 4, 7, 7, 6, 6, 5, 5, 4, 0, 5, 1, 6, 2, 7, 3, 4],
		dtype=uint32, )

	shader_data = {"buffer": {}, "constants": {}}

	GL.glBindVertexArray(GL.glGenVertexArrays(1))  # Have to do this first

	shader_data["buffer"]["vertices"] = GL.glGenBuffers(1)
	GL.glBindBuffer(GL.GL_ARRAY_BUFFER, shader_data["buffer"]["vertices"])
	GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_DYNAMIC_DRAW)

	stride = vertices.strides[0]
	offset = ctypes.c_void_p(0)

	loc = GL.glGetAttribLocation(program, "vertex_position")
	GL.glEnableVertexAttribArray(loc)
	GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, stride, offset)

	offset = ctypes.c_void_p(vertices.dtype["vertex_position"].itemsize)

	loc = GL.glGetAttribLocation(program, "vertex_colour")
	GL.glEnableVertexAttribArray(loc)
	GL.glVertexAttribPointer(loc, 4, GL.GL_FLOAT, False, stride, offset)

	shader_data["buffer"]["filled"] = GL.glGenBuffers(1)
	GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["filled"])
	GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, filled_cube_indices.nbytes, filled_cube_indices, GL.GL_STATIC_DRAW)

	shader_data["buffer"]["outline"] = GL.glGenBuffers(1)
	GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["outline"])
	GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, outline_cube_indices.nbytes, outline_cube_indices, GL.GL_STATIC_DRAW)

	shader_data["constants"]["model"] = GL.glGetUniformLocation(program, "model")
	GL.glUniformMatrix4fv(shader_data["constants"]["model"], 1, False, eye(4))

	shader_data["constants"]["view"] = GL.glGetUniformLocation(program, "view")
	view = translate(eye(4), z=-6)
	GL.glUniformMatrix4fv(shader_data["constants"]["view"], 1, False, view)

	shader_data["constants"]["projection"] = GL.glGetUniformLocation(program, "projection")
	GL.glUniformMatrix4fv(shader_data["constants"]["projection"], 1, False, eye(4))

	# This colour is multiplied with the base vertex colour in producing
	# the final output
	shader_data["constants"]["colour_mul"] = GL.glGetUniformLocation(program, "colour_mul")
	GL.glUniform4f(shader_data["constants"]["colour_mul"], 1, 1, 1, 1)

	# This colour is added on to the base vertex colour in producing
	# the final output
	shader_data["constants"]["colour_add"] = GL.glGetUniformLocation(program, "colour_add")
	GL.glUniform4f(shader_data["constants"]["colour_add"], 0, 0, 0, 0)

	# Set GL drawing data
	# -------------------
	GL.glClearColor(0, 0, 0, 0)
	GL.glPolygonOffset(1, 1)
	GL.glEnable(GL.GL_LINE_SMOOTH)
	GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
	GL.glDepthFunc(GL.GL_LESS)
	GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
	GL.glLineWidth(1.0)

	projection = perspective(45.0, display_size[0] / float(display_size[1]), 2.0, 100.0)
	GL.glUniformMatrix4fv(shader_data["constants"]["projection"], 1, False, projection)

	return shader_data, filled_cube_indices, outline_cube_indices


def draw_cube(p):
	shader_data, filled_cube_indices, outline_cube_indices, rotation = p
	"""
	Draw a cube in the 'modern' Open GL style, for post 3.1 versions of
	open GL.

	:param shader_data: compile vertex & pixel shader data for drawing a cube.
	:param filled_cube_indices: the indices to draw the 'filled' cube.
	:param outline_cube_indices: the indices to draw the 'outline' cube.
	:param rotation: the current rotations to apply.
	"""

	GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

	# Filled cube
	GL.glDisable(GL.GL_BLEND)
	GL.glEnable(GL.GL_DEPTH_TEST)
	GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
	GL.glUniform4f(shader_data["constants"]["colour_mul"], 1, 1, 1, 1)
	GL.glUniform4f(shader_data["constants"]["colour_add"], 0, 0, 0, 0.0)
	GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["filled"])
	GL.glDrawElements(GL.GL_TRIANGLES, len(filled_cube_indices), GL.GL_UNSIGNED_INT, None)

	# Outlined cube
	GL.glDisable(GL.GL_POLYGON_OFFSET_FILL)
	GL.glEnable(GL.GL_BLEND)
	GL.glUniform4f(shader_data["constants"]["colour_mul"], 0, 0, 0, 0.0)
	GL.glUniform4f(shader_data["constants"]["colour_add"], 1, 1, 1, 1.0)
	GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["outline"])
	GL.glDrawElements(GL.GL_LINES, len(outline_cube_indices), GL.GL_UNSIGNED_INT, None)

	# Rotate cube
	# rotation.theta += 1.0  # degrees
	rotation.phi += 1.0  # degrees
	# rotation.psi += 1.0  # degrees
	model = eye(4, dtype=float32)
	# rotate(model, rotation.theta, 0, 0, 1)
	rotate(model, rotation.phi, 0, 1, 0)
	rotate(model, rotation.psi, 1, 0, 0)
	GL.glUniformMatrix4fv(shader_data["constants"]["model"], 1, False, model)


def init_gl_rot(display_size):
	gpu, f_indices, o_indices = init_gl(display_size)
	rotation = Rotation()
	return gpu, f_indices, o_indices, rotation