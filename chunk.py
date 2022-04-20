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
		self.voxels = zeros(CHUNK_VOL, dtype=Voxel)
		for y in range(CHUNK_H):
			for z in range(CHUNK_D):
				for x in range(CHUNK_W):
	
					rx = x + self.x * CHUNK_W
					ry = y + self.y * CHUNK_H
					rz = z + self.z * CHUNK_D
				
					i_d = int(bool(ry <=((sin(radians(rx*15)))*192 + (cos(radians(rz*8)))*192)))
						
					if (ry <= 0):
						i_d = 2
					if (i_d > 2):
						i_d = 0
					if (i_d == 1 and ry%5 == 0):
						i_d = 2
					if (i_d == 1 and rz%5 == 0):
						i_d = 2
					elif(i_d == 2 and rz%5 == 0):
						i_d = 1 
					index = (y * CHUNK_D + z) * CHUNK_W + x 
					self.voxels[index] = Voxel(i_d)
