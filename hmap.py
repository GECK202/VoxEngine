from numpy import zeros, array, load, save
from chunk import Chunk, CHUNK_W, CHUNK_H, CHUNK_D
import voxel_renderer as vr
import hashlib


def get_name(hb):
	return f"env/cash/{hb}.npy"

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
		try:
			self.data = load("env/maparr.npy")
		except:
			self.data = zeros(w * h * d, dtype=object).reshape(w, h, d)
			for x in range(w):
				for y in range(h):
					print("save map[",x,y,"]")
					for z in range(d):
						self.save_buf(x, y, z)
			save("env/maparr.npy", self.data)
		print("Map buffers are cashed OK!")


	def save_buf(self, x, y, z):
		chunk = Chunk(x, y, z)
		chunk.full_up()
		buf = vr.VoxelRenderer.renderer.create_buf(chunk)
		#hb = hash(buf.data.tobytes())

		hb = hashlib.sha1(buf.data.tobytes()).hexdigest()
		#print(hash_object.hexdigest())

		shb = get_name(hb)
		save(shb, buf)
		self.data[x][y][z] = hb

	def load_buf(self, chunk):
		x = int(chunk.x / CHUNK_W)%10
		y = int(chunk.y / CHUNK_H)%8
		z = int(chunk.z / CHUNK_D)%10
		hb = self.data[x][y][z]
		shb = get_name(hb)
		try:
			buf = load(shb)
			return buf
		except:
			print("Error load map buffer [",x, y, z, "]", hb, shb)
			exit()