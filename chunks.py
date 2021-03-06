from numpy import zeros
from chunk import Chunk


class Chunks:
	chunks = None

	@classmethod
	def init(cls, w, d, h):
		if Chunks.chunks is None:
			Chunks.chunks = Chunks(w, d, h)
		return Chunks.chunks

	def __init__(self, w, d, h):
		self.w = w
		self.d = d
		self.h = h
		self.volume = w * d * h
		self.chunks = zeros(768, dtype=object)
		index = 0
		for y in range(h):
			for z in range(d):
				for x in range(w):
					self.chunks[index] = Chunk(x, y, z)
					index += 1
