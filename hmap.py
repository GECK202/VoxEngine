import os
from numpy import zeros, array, load, save
from chunk import Chunk, CHUNK_W, CHUNK_H, CHUNK_D
import voxel_renderer as vr

def get_name(hb):
	return "env/cash/" + str(hb).replace("-", "_") + ".npy"

class Hmap:
	h_map = None

	@classmethod
	def init(cls, w, h, d):
		if Hmap.h_map is None:
			Hmap.h_map = Hmap(w, h, d)
			vr.VoxelRenderer.init()
		return Hmap.h_map

	def __init__(self, w, h, d):
		print("Start cash map buffers...")
		self.w = w
		self.h = h
		self.d = d
		if not os.path.exists("env/cash"):
			os.mkdir("env/cash")
		try:
			self.data = load("env/maparr.npy")
			
		except:
			self.data = zeros(w * h * d, dtype=int).reshape(w, h, d)
			for x in range(w):
				for y in range(h):
					#print("save map[",x,y,"]")
					for z in range(d):
						self.save_buf(x, y, z)
			save("env/maparr.npy", self.data)
		#print("Map buffers are cashed OK!", self.save_buf)


	def save_buf(self, x, y, z):
		chunk = Chunk(x, y, z)
		chunk.full_up()
		buf = vr.VoxelRenderer.renderer.create_buf(chunk).reshape(-1)
		hb = hash(buf.data.tobytes())
		shb = get_name(hb)
		save(shb, buf)
		self.data[x][y][z] = hb

	def load_buf(self, chunk):
		x = int(chunk.x / CHUNK_W)%self.w
		y = int(chunk.y / CHUNK_H)%self.h
		z = int(chunk.z / CHUNK_D)%self.d
		hb = self.data[x][y][z]
		shb = get_name(hb)
		try:
			buf = load(shb).reshape(-1, 6, 6)
			print("-load mesh", int(chunk.x/CHUNK_W), int(chunk.y/CHUNK_H), int(chunk.z/CHUNK_D), shb)
			return buf
		except:
			#print("Error load map buffer [",x, y, z, "]", hb, shb)
			exit()