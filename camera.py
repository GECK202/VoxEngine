import glm
from glm import vec3, vec4, mat4, radians, lookAt, perspective
from numpy import array, eye, zeros, float32, uint32, transpose


from window import Window

class Camera:
	camera = None

	@classmethod
	def init(cls, pos, fov):
		if Camera.camera is None:
			Camera.camera = Camera(pos, fov)
		return Camera.camera

	def _update_vectors(self):
		self.front = vec3(self.rotation * vec4(0,0,-1,1))
		self.right = vec3(self.rotation * vec4(1,0,0,1))
		self.up = vec3(self.rotation * vec4(0,1,0,1))

	def __init__(self, pos, fov):
		self.pos = pos
		self.fov = fov
		self.rotation = mat4(1.0)
		self._update_vectors()

	def rotate(self, x, y, z):
		self.rotation = glm.rotate(self.rotation, z, vec3(0,0,1))
		self.rotation = glm.rotate(self.rotation, y, vec3(0,1,0))
		self.rotation = glm.rotate(self.rotation, x, vec3(1,0,0))
		self._update_vectors()

	def get_projection(self):
		aspect = Window.window.display_size[0] / Window.window.display_size[1]
		#print(Window.window.display_size)
		#print(aspect)
		return perspective(self.fov, aspect, 0.1, 100)

	def get_view(self):
		return lookAt(self.pos, self.pos + self.front, self.up)

	def get_m_proj_view(self):
		return transpose(array(self.get_projection() * self.get_view()))
