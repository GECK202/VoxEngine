from numpy import zeros, array, load, save
from chunk import Chunk
from voxel_renderer import VoxelRenderer


class Map:
	map = None

	@classmethod
	def init(cls, w, h, d):
		if Map.map is None:
			Map.map = Map(w, h, d)
			VoxelRenderer.init()
		return Map.map

	def __init__(self, w, h, d):
		self.data = zeros(w * h * d, dtype=int).reshape(w, h, d)
		print("start cash buffers...")
		for x in range(w):
			for y in range(h):
				for z in range(d):
					self.save_buf(x, y, z)
		print("buffers are cashed OK!")

	def save_buf(self, x, y, z):
		chunk = Chunk(x, y, z)
		buf = VoxelRenderer.renderer.create_buf(chunk)
		hb = hash(buf.data.tobytes())
		shb = "res/cash/" + str(hb).replace("-", "_") + ".npy"
		try:
			fbuf = load(shb)
		except:
			save(shb, buf)
		if fbuf.size != buf.size:
			hb = hash(hb)
			shb = "res/cash/" + str(hb).replace("-", "_") + ".npy"
		self.data[x][y][z] = hb

	def load_buf(self, chunk):
		load(Map[chunk.x][chunk.y][chunk.z] + ".npy")