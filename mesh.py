import ctypes
import OpenGL.GL as GL
from types import Dict
from numpy import uint8, uint32, array, zeros
from hashlib import sha1



class Mesh:
	
	mesh_dict:Dict[str, Mesh] = {}

	@classmethod
	def init(cls):
		buffer = zeros(0, dtype=float32)
		mesh = Mesh(buffer, 0, 6)
		hash_name = sha1(buffer.data.tobytes()).hexdigest()
		cls.mesh_dict[hash_name] = mesh


	@classmethod
	def add_mesh(cls, buffer: array, size: uint32) -> Mesh:
		hash_name = sha1(buffer.data.tobytes()).hexdigest()
		mesh: Mesh = cls.mesh_dict.get(hash_name)
		if mesh is None:
			mesh = Mesh(buffer, size, 6)
			cls.mesh_dict[hash_name] = mesh
		return mesh

	def __init__(self, buffer, vertices, attrs):
		#print(buffer)
		self.vertices = int(vertices)
		vertex_size = int(sum(attrs))
		#print(attrs)
		#print("vsize=",vertex_size,"  v=",self.vertices)

		#GL.glUseProgram(1)

		self.vao = GL.glGenVertexArrays(1)
		GL.glBindVertexArray(self.vao)

		self.vbo = GL.glGenBuffers(1)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

		GL.glBufferData(GL.GL_ARRAY_BUFFER, 4*vertex_size*self.vertices, buffer, GL.GL_STATIC_DRAW)
		#print(buffer)
		#print(self.vertices)
		# attributes
		offs = 0
		size = 0
		for i in range(len(attrs)):
			size = int(attrs[i])
			offset = ctypes.c_void_p(int(offs) * 4)
			#print("size=",size," offs=", offs)
			GL.glVertexAttribPointer(int(i), size, GL.GL_FLOAT, False, vertex_size * 4, offset)
			GL.glEnableVertexAttribArray(int(i))
			offs += size
		GL.glBindVertexArray(0)

	#def __del__(self):
	#	GL.glDeleteVertexArrays(1, self.vao)
	#	GL.glDeleteBuffers(1, self.vbo)

	def draw(self):#, primitive):
		GL.glBindVertexArray(self.vao)
		GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertices)
		GL.glBindVertexArray(0)
