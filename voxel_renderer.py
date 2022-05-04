from numpy import array, zeros, float32, uint32, append
from mesh import Mesh
import time

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
		dots = 6
		sides = 6
		BUF_SIZE = dots*sides*CHUNK_VOL
		self.buffer = zeros(VERTEX_SIZE*BUF_SIZE, dtype=float32).reshape(-1, 6, VERTEX_SIZE)

	def render(self, chunk):
		index = 0
		v_ind = -1

		uv = 1.0 / 16.0
		v0 = 0  # (id % 16) * uv

		#tmax = 0.0
		#tmin = 1.0
		#tmean = 0.0
		#count = 0
		s = time.perf_counter()
		for y in range(CHUNK_H):
			y0_ind = y*CHUNK_D
			#y1_ind=(y+1)*CHUNK_D
			#ym_ind=(y-1)*CHUNK_D
			#in_y0 = (y>=0 and y<CHUNK_H)
			#in_y1 = ((y+1)>=0 and (y+1)<CHUNK_H)
			#in_ym = ((y-1)>=0 and (y-1)<CHUNK_H)
			y05=y+0.5
			ym5=y-0.5

			for z in range(CHUNK_D):
				z00_ind=(y0_ind+z)*CHUNK_W
				#z01_ind=(y0_ind+z+1)*CHUNK_W
				#z0m_ind=(y0_ind+z-1)*CHUNK_W
				#z10_ind=(y1_ind+z)*CHUNK_W
				#z11_ind=(y1_ind+z+1)*CHUNK_W
				#z1m_ind=(y1_ind+z-1)*CHUNK_W
				#zm0_ind=(ym_ind+z)*CHUNK_W
				#zm1_ind=(ym_ind+z+1)*CHUNK_W
				#zmm_ind=(ym_ind+z-1)*CHUNK_W
				#in_z0 = (z>=0 and z < CHUNK_D)
				#in_z1 = ((z+1)>=0 and (z+1)<CHUNK_D)
				#in_zm = ((z-1)>=0 and (z-1)<CHUNK_D)
				z05=z+0.5
				zm5=z-0.5
				for x in range(CHUNK_W):
					v_ind = v_ind + 1
					vox = chunk.voxels[v_ind]
					if (vox.emp&0b1):
						continue
					#in_x0 = (x >= 0 and x < CHUNK_W)
					#in_x1 = ((x+1)>=0 and ((x+1)<CHUNK_W))
					#in_xm = ((x-1)>=0 and ((x-1)<CHUNK_W))
					x05=x+0.5
					xm5=x-0.5

					u0 = vox.id * uv  # 1-((1 + int(id / 16)) * uv)
					v1 = v0 + uv
					u1 = u0 + uv
					#if not(in_x0 and in_y1 and in_z0 and chunk.voxels[z10_ind+x].is_solid):#is_blocked(x,y+1,z,chunk)):
					s = chunk.voxels[z00_ind+x].emp
					if (s&0b100000)>>5:
						l = 1.0
						self.buffer[index]=array([
							[xm5, y05, zm5, u0,v0, l],[xm5, y05, z05, u0,v1, l],[x05, y05, z05, u1,v1, l],
							[xm5, y05, zm5, u0,v0, l],[x05, y05, z05, u1,v1, l],[x05, y05, zm5, u1,v0, l]], dtype=float32)
						index = index + 1
					#if not(in_x0 and in_ym and in_z0 and chunk.voxels[zm0_ind+x].is_solid):#is_blocked(x,y-1,z,chunk)):
					if (s&0b1000000)>>6:
						l = 0.75
						self.buffer[index] = array([
							[xm5, ym5, zm5, u0,v0, l],[x05, ym5, z05, u1,v1, l],[xm5, ym5, z05, u0,v1, l],
							[xm5, ym5, zm5, u0,v0, l],[x05, ym5, zm5, u1,v0, l],[x05, ym5, z05, u1,v1, l]], dtype=float32)
						index = index + 1
					#if not(in_x1 and in_y0 and in_z0 and chunk.voxels[z00_ind+x+1]):#is_blocked(x+1,y,z,chunk)):
					if (s&0b100)>>2:
						l = 0.95
						self.buffer[index] = array([
							[x05, ym5, zm5, u1,v1, l],[x05, y05, zm5, u1,v0, l],[x05, y05, z05, u0,v0, l],
							[x05, ym5, zm5, u1,v1, l],[x05, y05, z05, u0,v0, l],[x05, ym5, z05, u0,v1, l]], dtype=float32)
						index = index + 1
					#if not(in_xm and in_y0 and in_z0 and chunk.voxels[z00_ind+x-1].is_solid):#is_blocked(x-1,y,z,chunk)):
					if (s&0b10)>>1:
						l = 0.85
						self.buffer[index] = array([
							[xm5, ym5, zm5, u0,v1, l],[xm5, y05, z05, u1,v0, l],[xm5, y05, zm5, u0,v0, l],
							[xm5, ym5, zm5, u0,v1, l],[xm5, ym5, z05, u1,v1, l],[xm5, y05, z05, u1,v0, l]], dtype=float32)
						index = index + 1
					#if not(in_x0 and in_y0 and in_z1 and chunk.voxels[z01_ind+x].is_solid):#is_blocked(x,y,z+1,chunk)):
					if (s&0b1000)>>3:
						l = 0.9
						self.buffer[index] = array([
							[xm5, ym5, z05, u0,v1, l],[x05, y05, z05, u1,v0, l],[xm5, y05, z05, u0,v0, l],
							[xm5, ym5, z05, u0,v1, l],[x05, ym5, z05, u1,v1, l],[x05, y05, z05, u1,v0, l]], dtype=float32)
						index = index + 1
					#if not(in_x0 and in_y0 and in_zm and chunk.voxels[zm0_ind+x].is_solid):#is_blocked(x,y,z-1,chunk)):
					if (s&10000)>>4:
						l = 0.8
						self.buffer[index] = array([
							[xm5, ym5, zm5, u1,v1, l],[xm5, y05, zm5, u1,v0, l],[x05, y05, zm5, u0,v0, l],
							[xm5, ym5, zm5, u1,v1, l],[x05, y05, zm5, u0,v0, l],[x05, ym5, zm5, u0,v1, l]], dtype=float32)
						index = index + 1
		#d = time.perf_counter() - s
		#if d > tmax:
		#	tmax = d
		#if d < tmin:
		#	tmin = d
		#tmean += d
		#count += 1
		#print("min=", tmin, "max=", tmax, "mean=", tmean/count)
		m = Mesh(self.buffer, index*6, chunk_attrs)
		#d = time.perf_counter() - s
		#print("timing=", d)
		return m