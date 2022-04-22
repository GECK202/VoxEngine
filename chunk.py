from numpy import zeros
from math import sin, cos
from glm import vec3, vec4, mat4, radians


CHUNK_W, CHUNK_H, CHUNK_D = 64,64,64#16, 16, 16
CHUNK_VOL = CHUNK_H * CHUNK_W * CHUNK_D

class Voxel:
	def __init__(self, i_d):
		self.id = i_d
		is_solid = True
		if i_d == 0:
			is_solid = False
		self.is_solid = is_solid

class Chunk:
	def __init__(self, ix, iy, iz):
		self.x = ix
		self.y = iy
		self.z = iz
		self.modified = True
		self.voxels = zeros(CHUNK_VOL, dtype=object)
		index = 0
		for y in range(CHUNK_H):
			ry = y + self.y * CHUNK_H
			ry5 = (ry%5 == 0)
			for z in range(CHUNK_D):
				rz = z + self.z * CHUNK_D
				cos_z=cos(radians(rz*8))*192
				rz5 = (rz%5 == 0)
				for x in range(CHUNK_W):
	
					
					
					if (ry <= 0):
						i_d = 2
					else:
						rx = x + self.x * CHUNK_W
						i_d = int((ry <=((sin(radians(rx*15)))*192 + cos_z)))
						if (i_d > 2):
							i_d = 0
						
					
					
					if (ry5 or rz5) and (i_d > 0):
						i_d = i_d%2 + 1
					#index = (y * CHUNK_D + z) * CHUNK_W + x 
					self.voxels[index] = Voxel(i_d)
					index += 1
