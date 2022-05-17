from PIL import Image
from numpy import array, zeros, int8, load, save

class Tile:
	tile = None

	@classmethod
	def init(cls):
		if Tile.tile is None:
			Tile.tile = Tile()
		return Tile.tile

	def __init__(self):
		print("Start generate tile, please wait...")
		try:
			self.newData = load("env/tilearr.npy")
		except:
			im = Image.open("res/perlin_noise.png")
			data = array(im.getdata())
			self.newData = zeros(1024*1024*256, dtype=int8).reshape(1024,256,1024)
			for x in range(1024):
				xi = x * 1024
				for z in range(1024):
					dot = data[xi+z]
				#pos = 4
				#if dot<pos:
				#	pos = dot
				#for y in range(pos):
				#	self.newData[x][y][z]=2
					for y in range(dot):
						self.newData[x][y][z]=1
			#print(self.newData)
			save("env/tilearr.npy", self.newData)
		print("End generate tile. It is OK.")

	def _get_id(self, x,y,z,d):
		kx = (1024 + x) % 1024
		ky = (256 + y) % 256 
		kz = (1024 + z) % 1024
		#print(kx, ky, kz, self.newData[kx][ky][kz])
		a = int(not(bool(self.newData[kx][ky][kz])))

		return a<<d

	def getID(self, x,y,z):

		id0 = self._get_id(x,y,z,0)
		id1 = self._get_id(x - 1, y, z, 1)
		id2 = self._get_id(x + 1, y, z, 2)
		id3 = self._get_id(x, y, z + 1, 3)
		id4 = self._get_id(x, y, z - 1, 4)
		id5 = self._get_id(x, y + 1, z, 5)
		id6 = self._get_id(x, y - 1, z, 6)
		#print("data=",self.newData[x][y][z], "x y z",x,y,z,"id=",id0,id1,id2,id3,id4,id5,id6)
		return id0|id1|id2|id3|id4|id5|id6

