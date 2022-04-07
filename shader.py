import OpenGL.GL as GL

class Shader:

	@staticmethod
	def _file_to_str(filename):
		with open(filename, 'r') as my_file:
			data = my_file.read()
		return data

	def __init__(self, ver_file_name, frag_file_name):
		self.program = Shader._load_shader(ver_file_name, frag_file_name)

	def use(self):
		GL.glUseProgram(self.program)

	def __del__(self):
		GL.glDeleteProgram(self.program)

	@staticmethod
	def _info_log(log):
		print(log)
		return None

	@staticmethod
	def _load_shader(vert_file_name, frag_file_name):
		vertex_code = Shader._file_to_str(vert_file_name)
		fragment_code = Shader._file_to_str(frag_file_name)

		#создание вершинного шейдера
		vertex = GL.glCreateShader(GL.GL_VERTEX_SHADER)
		GL.glShaderSource(vertex, vertex_code)
		GL.glCompileShader(vertex)
		log = GL.glGetShaderInfoLog(vertex)
		if isinstance(log, bytes):
			return Shader._info_log(log.decode())

		#создание фрагментного шейдера
		fragment = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
		GL.glShaderSource(fragment, fragment_code)
		GL.glCompileShader(fragment)
		log = GL.glGetShaderInfoLog(fragment)
		if isinstance(log, bytes):
			return Shader._info_log(log.decode())

		#создание шейдерной программы
		program = GL.glCreateProgram()
		GL.glAttachShader(program, vertex)
		GL.glAttachShader(program, fragment)
		GL.glValidateProgram(program)
		GL.glLinkProgram(program)

		GL.glDetachShader(program, vertex)
		GL.glDetachShader(program, fragment)

		log = GL.glGetProgramInfoLog(program)
		if isinstance(log, bytes):
			return Shader._info_log(log.decode())

		#GL.glUseProgram(program)
		return program

