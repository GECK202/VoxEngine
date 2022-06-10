from numpy import array, zeros, float32, uint32, append
from mesh import Mesh

VERTEX_SIZE = 3 + 2
CHUNK_W, CHUNK_H, CHUNK_D = 64,64,64#16, 16, 16
CHUNK_VOL = CHUNK_W*CHUNK_H*CHUNK_D

chunk_attrs = array([3,2])

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
	
	def add_vertex(self, index, x, y, z, u, v):
		#print("index=",index,"[",x,y,z,u,v,l,"]")
		
		self.buffer[index+0]=x
		self.buffer[index+1]=y
		self.buffer[index+2]=z
		self.buffer[index+3]=u
		self.buffer[index+4]=v
		#self.buffer[index+5]=l
		#print(self.buffer)
		return index + 5

	def render(self, chunk):
		index = 0
		v_ind = -1
		uv = 1.0 / 16.0
		
		for y in range(CHUNK_H):
			#print(y)
			y1_ind=(y+1)*CHUNK_D
			ym_ind=(y-1)*CHUNK_D
			in_y = (y>=0 and y<CHUNK_H)
			in_y1 = ((y+1)>=0 and (y+1)<CHUNK_H)
			in_ym = ((y-1)>=0 and (y-1)<CHUNK_H)
			y05 = y + 0.5
			ym5 = y - 0.5
			for z in range(CHUNK_D):
				#print(z)
				z11_ind=(y1_ind+z+1)*CHUNK_W
				z1m_ind=(y1_ind+z-1)*CHUNK_W
				zm1_ind=(ym_ind+z+1)*CHUNK_W
				zmm_ind=(ym_ind+z-1)*CHUNK_W
				in_z1 = ((z+1)>=0 and (z+1)<CHUNK_D)
				in_zm = ((z-1)>=0 and (z-1)<CHUNK_D)
				z05 = z + 0.5
				zm5 = z - 0.5
				for x in range(CHUNK_W):
					v_ind = v_ind + 1

					vox = chunk.voxels[v_ind]
					#print(z_ind + x)
					if not(vox.is_solid):
						continue
					i_d = vox.id
					x05 = x + 0.5
					xm5 = x - 0.5
					#v = 0 #(id % 16) * uv
					u00 = (i_d % 5) * uv * 3 #1-((1 + int(id / 16)) * uv)
					u01 = u00 + uv
					u11 = u01 + uv
					u22 = u11 + uv
					v00 = (i_d // 5) * uv * 2
					v01 = v00 + uv
					v11 = v01 + uv
					if not(is_blocked(x,y+1,z,chunk)):
						index = self.add_vertex(index, xm5, y05, zm5, u00,v00)
						index = self.add_vertex(index, xm5, y05, z05, u00,v01)
						index = self.add_vertex(index, x05, y05, z05, u01,v01)

						index = self.add_vertex(index, xm5, y05, zm5, u00,v00)
						index = self.add_vertex(index, x05, y05, z05, u01,v01)
						index = self.add_vertex(index, x05, y05, zm5, u01,v00)
						
					if not(is_blocked(x,y-1,z,chunk)):
						index = self.add_vertex(index, xm5, ym5, zm5, u11,v11)
						index = self.add_vertex(index, x05, ym5, z05, u22,v01)
						index = self.add_vertex(index, xm5, ym5, z05, u11,v01)
						
						index = self.add_vertex(index, xm5, ym5, zm5, u11,v11)
						index = self.add_vertex(index, x05, ym5, zm5, u22,v11)
						index = self.add_vertex(index, x05, ym5, z05, u22,v01)
						
					if not(is_blocked(x+1,y,z,chunk)):
						index = self.add_vertex(index, x05, ym5, zm5, u22,v01)
						index = self.add_vertex(index, x05, y05, zm5, u22,v00)
						index = self.add_vertex(index, x05, y05, z05, u11,v00)

						index = self.add_vertex(index, x05, ym5, zm5, u22,v01)
						index = self.add_vertex(index, x05, y05, z05, u11,v00)
						index = self.add_vertex(index, x05, ym5, z05, u11,v01)
				
					if not(is_blocked(x-1,y,z,chunk)):
						index = self.add_vertex(index, xm5, ym5, zm5, u01,v01)
						index = self.add_vertex(index, xm5, y05, z05, u11,v00)
						index = self.add_vertex(index, xm5, y05, zm5, u01,v00)

						index = self.add_vertex(index, xm5, ym5, zm5, u01,v01)
						index = self.add_vertex(index, xm5, ym5, z05, u11,v01)
						index = self.add_vertex(index, xm5, y05, z05, u11,v00)
				
					if not(is_blocked(x,y,z+1,chunk)):
						index = self.add_vertex(index, xm5, ym5, z05, u01,v11)
						index = self.add_vertex(index, x05, y05, z05, u11,v01)
						index = self.add_vertex(index, xm5, y05, z05, u01,v01)

						index = self.add_vertex(index, xm5, ym5, z05, u01,v11)
						index = self.add_vertex(index, x05, ym5, z05, u11,v11)
						index = self.add_vertex(index, x05, y05, z05, u11,v01)
				
					if not(is_blocked(x,y,z-1,chunk)):
						index = self.add_vertex(index, xm5, ym5, zm5, u01,v11)
						index = self.add_vertex(index, xm5, y05, zm5, u01,v01)
						index = self.add_vertex(index, x05, y05, zm5, u00,v01)

						index = self.add_vertex(index, xm5, ym5, zm5, u01,v11)
						index = self.add_vertex(index, x05, y05, zm5, u00,v01)
						index = self.add_vertex(index, x05, ym5, zm5, u00,v11)
		#print(self.buffer)
		return Mesh(self.buffer, index / VERTEX_SIZE, chunk_attrs)
