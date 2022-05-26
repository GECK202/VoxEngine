from numpy import zeros, uint32

from tile import Tile, TILE_X, TILE_Y, TILE_Z

CHUNK_W, CHUNK_H, CHUNK_D = 34, 34, 34
CHUNK_VOL = CHUNK_H * CHUNK_W * CHUNK_D

#class Voxel:
#	def __init__(self, i_d, emp):
#		self.i_d = i_d
#		self.emp = emp

class Chunk:

	def set_start(self):
		index = 0
		tile = Tile.init()
		#st = set()
		#print("TILE=",tile.newData)
		for y in range(CHUNK_H):
			ry = (self.y + y - 1) % TILE_Y
			for z in range(CHUNK_D):
				rz = (self.z + z - 1) % TILE_Z
				for x in range(CHUNK_W):
					rx = (self.x + x - 1) % TILE_X
					self.voxels[index] = tile.newData[rx][ry][rz]
					index += 1
		#print(st)

	def __init__(self, ix, iy, iz):
		#iy *= CHUNK_H
		#iz *= CHUNK_D
		#ix *= CHUNK_W
		self.x = ix
		self.y = iy
		self.z = iz
		self.modified = True
		self.voxels = zeros(CHUNK_VOL, dtype = uint8)#object)
		self.mesh = None


