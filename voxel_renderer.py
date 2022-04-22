from numpy import array, zeros, float32, uint32, append
from mesh import Mesh

VERTEX_SIZE = 3 + 2 + 1
CHUNK_W, CHUNK_H, CHUNK_D = 64,64,64#16, 16, 16
CHUNK_VOL = CHUNK_W*CHUNK_H*CHUNK_D

chunk_attrs = array([3,2,1])

def is_in(x, y, z):
	return bool(x>=0 and x<CHUNK_W and y>=0 and y<CHUNK_H and z>=0 and z<CHUNK_D)

def voxel_index(x, y, z):
	return ((y*CHUNK_D+z)*CHUNK_W+x)

def is_blocked(x, y, z, chunk):
	return bool(is_in(x ,y, z) and chunk.voxels[voxel_index(x, y, z)].is_solid)

class VoxelRenderer:
	renderer = None

	@classmethod
	def init(cls):#, capacity):
		if VoxelRenderer.renderer is None:
			VoxelRenderer.renderer = VoxelRenderer()#capacity)
		return VoxelRenderer.renderer

	def __init__(self):#, capacity):
		self.buffer = zeros(VERTEX_SIZE*6*6*CHUNK_VOL, dtype=float32)
	
	def add_vertex(self, index, x, y, z, u, v, l):
		#print("index=",index,"[",x,y,z,u,v,l,"]")
		
		self.buffer[index+0]=x
		self.buffer[index+1]=y
		self.buffer[index+2]=z
		self.buffer[index+3]=u
		self.buffer[index+4]=v
		self.buffer[index+5]=l
		#print(self.buffer)
		return

	def render(self, chunk):
		index = 0
		v_ind = -1
		for y in range(CHUNK_H):
			#print(y)
			y1_ind=(y+1)*CHUNK_D
			ym_ind=(y-1)*CHUNK_D
			in_y = (y>=0 and y<CHUNK_H)
			in_y1 = ((y+1)>=0 and (y+1)<CHUNK_H)
			in_ym = ((y-1)>=0 and (y-1)<CHUNK_H)
			for z in range(CHUNK_D):
				#print(z)
				z11_ind=(y1_ind+z+1)*CHUNK_W
				z1m_ind=(y1_ind+z-1)*CHUNK_W
				zm1_ind=(ym_ind+z+1)*CHUNK_W
				zmm_ind=(ym_ind+z-1)*CHUNK_W
				in_z1 = ((z+1)>=0 and (z+1)<CHUNK_D)
				in_zm = ((z-1)>=0 and (z-1)<CHUNK_D)
				for x in range(CHUNK_W):
					v_ind = v_ind + 1

					vox = chunk.voxels[v_ind]
					#print(z_ind + x)
					if not(vox.is_solid):
						continue
					i_d = vox.id
					l = 0
					uv = 1.0/16.0
					v = 0 #(id % 16) * uv
					u = i_d * uv #1-((1 + int(id / 16)) * uv)
					if not(is_blocked(x,y+1,z,chunk)):
						l = 1.0
						self.add_vertex(index, x - 0.5, y + 0.5, z - 0.5, u,v, l)
						self.add_vertex(index, x - 0.5, y + 0.5, z + 0.5, u,v+uv, l)
						self.add_vertex(index, x + 0.5, y + 0.5, z + 0.5, u+uv,v+uv, l)

						self.add_vertex(index, x - 0.5, y + 0.5, z - 0.5, u,v, l)
						self.add_vertex(index, x + 0.5, y + 0.5, z + 0.5, u+uv,v+uv, l)
						self.add_vertex(index, x + 0.5, y + 0.5, z - 0.5, u+uv,v, l)
						index = index + 6
					if not(is_blocked(x,y-1,z,chunk)):
						l = 0.75
						index = self.add_vertex(index, x - 0.5, y - 0.5, z - 0.5, u,v, l)
						index = self.add_vertex(index, x + 0.5, y - 0.5, z + 0.5, u+uv,v+uv, l)
						index = self.add_vertex(index, x - 0.5, y - 0.5, z + 0.5, u,v+uv, l)
						
						index = self.add_vertex(index, x - 0.5, y - 0.5, z - 0.5, u,v, l)
						index = self.add_vertex(index, x + 0.5, y - 0.5, z - 0.5, u+uv,v, l)
						index = self.add_vertex(index, x + 0.5, y - 0.5, z + 0.5, u+uv,v+uv, l)
						
					if not(is_blocked(x+1,y,z,chunk)):
						l = 0.95
						index = self.add_vertex(index, x + 0.5, y - 0.5, z - 0.5, u+uv,v+uv, l)
						index = self.add_vertex(index, x + 0.5, y + 0.5, z - 0.5, u+uv,v, l)
						index = self.add_vertex(index, x + 0.5, y + 0.5, z + 0.5, u,v, l)

						index = self.add_vertex(index, x + 0.5, y - 0.5, z - 0.5, u+uv,v+uv, l)
						index = self.add_vertex(index, x + 0.5, y + 0.5, z + 0.5, u,v, l)
						index = self.add_vertex(index, x + 0.5, y - 0.5, z + 0.5, u,v+uv, l)
				
					if not(is_blocked(x-1,y,z,chunk)):
						l = 0.85
						index = self.add_vertex(index, x - 0.5, y - 0.5, z - 0.5, u,v+uv, l)
						index = self.add_vertex(index, x - 0.5, y + 0.5, z + 0.5, u+uv,v, l)
						index = self.add_vertex(index, x - 0.5, y + 0.5, z - 0.5, u,v, l)

						index = self.add_vertex(index, x - 0.5, y - 0.5, z - 0.5, u,v+uv, l)
						index = self.add_vertex(index, x - 0.5, y - 0.5, z + 0.5, u+uv,v+uv, l)
						index = self.add_vertex(index, x - 0.5, y + 0.5, z + 0.5, u+uv,v, l)
				
					if not(is_blocked(x,y,z+1,chunk)):
						l = 0.9
						index = self.add_vertex(index, x - 0.5, y - 0.5, z + 0.5, u,v+uv, l)
						index = self.add_vertex(index, x + 0.5, y + 0.5, z + 0.5, u+uv,v, l)
						index = self.add_vertex(index, x - 0.5, y + 0.5, z + 0.5, u,v, l)

						index = self.add_vertex(index, x - 0.5, y - 0.5, z + 0.5, u,v+uv, l)
						index = self.add_vertex(index, x + 0.5, y - 0.5, z + 0.5, u+uv,v+uv, l)
						index = self.add_vertex(index, x + 0.5, y + 0.5, z + 0.5, u+uv,v, l)
				
					if not(is_blocked(x,y,z-1,chunk)):
						l = 0.8
						index = self.add_vertex(index, x - 0.5, y - 0.5, z - 0.5, u+uv,v+uv, l)
						index = self.add_vertex(index, x - 0.5, y + 0.5, z - 0.5, u+uv,v, l)
						index = self.add_vertex(index, x + 0.5, y + 0.5, z - 0.5, u,v, l)

						index = self.add_vertex(index, x - 0.5, y - 0.5, z - 0.5, u+uv,v+uv, l)
						index = self.add_vertex(index, x + 0.5, y + 0.5, z - 0.5, u,v, l)
						index = self.add_vertex(index, x + 0.5, y - 0.5, z - 0.5, u,v+uv, l)
		#print(self.buffer)
		return Mesh(self.buffer, index / VERTEX_SIZE, chunk_attrs)