from numpy import zeros
from math import sin, cos
from glm import vec3, vec4, mat4, radians


CHUNK_W, CHUNK_H, CHUNK_D = 64,256,64#16, 16, 16
CHUNK_VOL = CHUNK_H * CHUNK_W * CHUNK_D

class Voxel:
	def __init__(self, i_d, is_solid):
		self.id = i_d
		self.is_solid = is_solid

class Chunk:

	def __init__(self):
		self.voxels = zeros(CHUNK_VOL, dtype=Voxel)
		for y in range(CHUNK_H):
			for z in range(CHUNK_D):
				for x in range(CHUNK_W):
					i_d = int(bool(y <=((sin(radians(x*15)))*128 + (cos(radians(z*8)))*128)))
					if (y <= 0):
						i_d = 2
					if (i_d > 2):
						i_d = 0
					if (i_d == 1 and y%5 == 0):
						i_d = 2
					if (i_d == 1 and z%5 == 0):
						i_d = 2
					elif(i_d == 2 and z%5 == 0):
						i_d = 1 
					index = (y * CHUNK_D + z) * CHUNK_W + x 
					is_solid = False
					if i_d>0:
						is_solid = True
					#print("chunk = [",x,y,z,i_d,is_solid,"]")
					self.voxels[index] = Voxel(i_d, is_solid)
