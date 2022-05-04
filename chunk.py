from numpy import zeros, array, int8
from math import sin, cos
from glm import vec3, vec4, mat4, radians

from PIL import Image

from tile import Tile

CHUNK_W, CHUNK_H, CHUNK_D = 64,64,64#16, 16, 16
CHUNK_VOL = CHUNK_H * CHUNK_W * CHUNK_D

class Voxel:
	def __init__(self, id, emp):
		self.id = id
		self.emp = emp

def get_id(ry, x, sx, cos_z, d):
	if (ry <= 0):
		i_d = 1
	else:
		rx = x + sx * CHUNK_W
		i_d = int((ry <= ((sin(radians(rx * 15))) * 192 + cos_z)))
		if (i_d > 2):
			i_d = 0
	if i_d>0:
		i_d = 0b0<<d
	else:
		i_d = 0b1<<d
	return i_d

def get_id2(x,y,z):
	tile = Tile.init()
	return tile.getID(x,y,z)

class Chunk:
	def __init__(self, ix, iy, iz):
		iy *= CHUNK_H
		iz *= CHUNK_D
		ix *= CHUNK_W
		self.x = ix
		self.y = iy
		self.z = iz
		self.modified = True
		self.voxels = zeros(CHUNK_VOL, dtype=object)
		index = 0
		tile = Tile.init()
		#iy += 100
		for y in range(CHUNK_H):
			ry = iy + y
			#ry1 = ry+1
			#rym = ry-1
			#ry5 = (ry%5 == 0)

			for z in range(CHUNK_D):
				rz = iz + z
				#rz1 = rz+1
				#rzm = rz-1
				#cos_z=cos(radians(rz*8))*192
				#cos_z1=cos(radians(rz1*8)*192)
				#cos_zm=cos(radians(rzm*8)*192)
				#rz5 = (rz%5 == 0)
				for x in range(CHUNK_W):
					rx = ix + x
					#idc = get_id(ry,x,self.x,cos_z,0)
					#idc = idc|get_id(ry,x+1,self.x,cos_z,1)
					#idc = idc|get_id(ry, x-1, self.x, cos_z,2)
					#idc = idc|get_id(ry, x, self.x, cos_z1,3)
					#idc = idc|get_id(ry, x, self.x, cos_zm,4)
					#idc = idc|get_id(ry1, x, self.x, cos_z,5)
					#idc = idc|get_id(rym, x, self.x, cos_z,6)
					#print("idc =",idc)
					#if (ry <= 0):
					#	i_d = 2
					#else:
					#	rx = x + self.x * CHUNK_W
					#	i_d = int((ry <= ((sin(radians(rx * 15))) * 192 + cos_z)))
					#	if (i_d > 2):
					#		i_d = 0

					#if (ry5 or rz5) and (i_d > 0):
					#i_d = i_d%2 + 1
					#index = (y * CHUNK_D + z) * CHUNK_W + x 
					id = tile.newData[rx][ry][rz]
					if (id == 1) and ((ry%5) and (rx%7) and (rz%11)) == 0:
						id = 2
					#if id == 0:
					#	if iy < 4:
					#		id = 2
					#	else:
					#		id = 1
					#else:
					#	id = 0
					#if id > 0:
					emp = tile.getID(rx, ry, rz)
					#print(emp)
					#else:
					#	emp = 0
					self.voxels[index] = Voxel(id, emp)
					index += 1
		#print(rx, ry, rz, self.voxels[index-1].emp)