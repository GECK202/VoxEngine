import glm
from numpy import array, eye, zeros, float32, uint32
from window import Window

class Camera:
	camera = None

	@classmethod
	def init(cls, pos):
		if Camera.camera is None:
			Camera.camera = Camera(pos)
		return Camera.camera

	def _update_vectors(self):
		self.up = glm.vec3(self.rotation * glm.vec4(0,1,0,1))
		self.front = glm.vec3(self.rotation * glm.vec4(0,0,-1,1))
		self.right = glm.vec3(self.rotation * glm.vec4(1,0,0,1))

	def __init__(self, pos = glm.vec3(0,0,0), fov = 70.0, rotation = glm.mat4(1.0)):
		self.pos = pos
		self.fov = fov
		self.rotation = rotation
		self._update_vectors()
		
	def get_view(self):
		return glm.lookAt(self.pos, self.pos + self.front, self.up)

	def get_m_proj_view(self):
		return array(self.get_projection() * self.get_view())

	def get_projection(self):
		aspect = Window.window.display_size[0] / Window.window.display_size[1]
		return glm.perspective(self.fov, aspect, 0.1, 100)

	def rotate(self, x, y, z):
		self.rotation = glm.rotate(self.rotation, z, glm.vec3(0,0,1))
		self.rotation = glm.rotate(self.rotation, y, glm.vec3(0,1,0))
		self.rotation = glm.rotate(self.rotation, x, glm.vec3(1,0,0))
		self._update_vectors()
