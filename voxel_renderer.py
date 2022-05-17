from numpy import array, zeros, float32, save, load
from mesh import Mesh
import hmap

VERTEX_SIZE = 3 + 2 + 1
CHUNK_W, CHUNK_H, CHUNK_D = 32,32,32
CHUNK_VOL = CHUNK_W * CHUNK_H * CHUNK_D

chunk_attrs = array([3, 2, 1])


# def is_in(x, y, z):
#	return bool(x >= 0 and x < CHUNK_W and y >= 0 and y < CHUNK_H and z >= 0 and z < CHUNK_D)


# def voxel_index(x, y, z):
#	return ((y * CHUNK_D + z) * CHUNK_W + x)


# def is_blocked(x, y, z, chunk):
#	return bool(is_in(x, y, z) and chunk.voxels[voxel_index(x, y, z)].is_solid)


def render(chunk):
	buff = hmap.Hmap.h_map.load_buf(chunk)
	
	index = int(buff.size / 6)
	#print(index)
	return Mesh(buff, index, chunk_attrs)


class VoxelRenderer:
	renderer = None
	#_buf_number = -1

	#@classmethod
	#def get_buf_number(cls):
	#	VoxelRenderer._buf_number += 1
	#	return VoxelRenderer._buf_number

	@classmethod
	def init(cls):  # , capacity):
		if VoxelRenderer.renderer is None:
			VoxelRenderer.renderer = VoxelRenderer()  # capacity)
		return VoxelRenderer.renderer

	def __init__(self):  # , capacity):
		dots = 6
		sides = 6
		BUF_SIZE = dots * sides * CHUNK_VOL
		self.buffer = zeros(VERTEX_SIZE * BUF_SIZE, dtype=float32).reshape(-1, 6, VERTEX_SIZE)

	def create_buf(self, chunk):
		#dots = 6
		#sides = 6
		#BUF_SIZE = dots * sides * CHUNK_VOL
		#self.buff = zeros(VERTEX_SIZE * BUF_SIZE, dtype=float32).reshape(-1, 6, VERTEX_SIZE)

		index = 0
		v_ind = -1

		uv = 1.0 / 16.0
		v0 = 0
		for y in range(CHUNK_H):
			y0_ind = y * CHUNK_D
			y05 = y + 0.5
			ym5 = y - 0.5
			for z in range(CHUNK_D):
				z00_ind = (y0_ind + z) * CHUNK_W
				z05 = z + 0.5
				zm5 = z - 0.5
				for x in range(CHUNK_W):
					v_ind = v_ind + 1
					vox = chunk.voxels[v_ind]
					if vox.emp & 0b1:
						continue
					x05 = x + 0.5
					xm5 = x - 0.5
					u0 = vox.i_d * uv
					v1 = v0 + uv
					u1 = u0 + uv
					s = chunk.voxels[z00_ind + x].emp
					#print(x,y,z,s)
					if (s & 0b100000) >> 5:
						lt = 1.0
						self.buffer[index] = array([
							[xm5, y05, zm5, u0, v0, lt], [xm5, y05, z05, u0, v1, lt], [x05, y05, z05, u1, v1, lt],
							[xm5, y05, zm5, u0, v0, lt], [x05, y05, z05, u1, v1, lt], [x05, y05, zm5, u1, v0, lt]],
							dtype=float32)
						index = index + 1
					if (s & 0b1000000) >> 6:
						lt = 0.65
						self.buffer[index] = array([
							[xm5, ym5, zm5, u0, v0, lt], [x05, ym5, z05, u1, v1, lt], [xm5, ym5, z05, u0, v1, lt],
							[xm5, ym5, zm5, u0, v0, lt], [x05, ym5, zm5, u1, v0, lt], [x05, ym5, z05, u1, v1, lt]],
							dtype=float32)
						index = index + 1
					if (s & 0b100) >> 2:
						lt = 0.85
						self.buffer[index] = array([
							[x05, ym5, zm5, u1, v1, lt], [x05, y05, zm5, u1, v0, lt], [x05, y05, z05, u0, v0, lt],
							[x05, ym5, zm5, u1, v1, lt], [x05, y05, z05, u0, v0, lt], [x05, ym5, z05, u0, v1, lt]],
							dtype=float32)
						index = index + 1
					if (s & 0b10) >> 1:
						lt = 0.75
						self.buffer[index] = array([
							[xm5, ym5, zm5, u0, v1, lt], [xm5, y05, z05, u1, v0, lt], [xm5, y05, zm5, u0, v0, lt],
							[xm5, ym5, zm5, u0, v1, lt], [xm5, ym5, z05, u1, v1, lt], [xm5, y05, z05, u1, v0, lt]],
							dtype=float32)
						index = index + 1
					if (s & 0b1000) >> 3:
						lt = 0.9
						self.buffer[index] = array([
							[xm5, ym5, z05, u0, v1, lt], [x05, y05, z05, u1, v0, lt], [xm5, y05, z05, u0, v0, lt],
							[xm5, ym5, z05, u0, v1, lt], [x05, ym5, z05, u1, v1, lt], [x05, y05, z05, u1, v0, lt]],
							dtype=float32)
						index = index + 1
					if (s & 10000) >> 4:
						lt = 0.8
						self.buffer[index] = array([
							[xm5, ym5, zm5, u1, v1, lt], [xm5, y05, zm5, u1, v0, lt], [x05, y05, zm5, u0, v0, lt],
							[xm5, ym5, zm5, u1, v1, lt], [x05, y05, zm5, u0, v0, lt], [x05, ym5, zm5, u0, v1, lt]],
							dtype=float32)
						index = index + 1
		#b = self.buff[:index]
		#	print("MESH INDEX=",index)
		return self.buffer[:index]
		#hb = hash(b.data.tobytes())
		#Map.map[chunk.x % CHUNK_W][chunk.y % CHUNK_H][chunk.z % CHUNK_D] = hb
		#shb = str(hb).replace("-", "_") + ".npy"
		#bf = None
		#try:
		#	bf = load(shb)
		#except:
		#	save(shb, b)
		#if (not (bf is None)) and (bf != b):
		#
		#chunk.buf_name = str(VoxelRenderer.get_buf_number())
		#save(b, chunk.buf_name)
