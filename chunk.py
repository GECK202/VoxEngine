from numpy import zeros

from tile import Tile

CHUNK_W, CHUNK_H, CHUNK_D = 32,32,32
CHUNK_VOL = CHUNK_H * CHUNK_W * CHUNK_D

class Voxel:
	def __init__(self, i_d, emp):
		self.i_d = i_d
		self.emp = emp

class Chunk:

	def full_up(self):
		index = 0
		tile = Tile.init()
		for y in range(CHUNK_H):
			ry = (self.y + y) % 256
			for z in range(CHUNK_D):
				rz = (self.z + z) % 1024
				for x in range(CHUNK_W):
					rx = (self.x + x) % 1024
					i_d = tile.newData[rx][ry][rz]
					if (i_d == 1) and ((ry % 5) and (rx % 7) and (rz % 11)) == 0:
						i_d = 2
					emp = tile.getID(rx, ry, rz)
					self.voxels[index] = Voxel(i_d, emp)
					index += 1

	def __init__(self, ix, iy, iz):
		iy *= CHUNK_H
		iz *= CHUNK_D
		ix *= CHUNK_W
		self.x = ix
		self.y = iy
		self.z = iz
		self.modified = True
		self.voxels = zeros(CHUNK_VOL, dtype=object)


