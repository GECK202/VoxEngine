import ctypes

import pygame as pg
from window import Window
from events import Events
from shader import Shader

import OpenGL.GL as GL

from glm import vec3, vec4, mat4, radians, translate
#from ogl3 import init_gl_rot, draw_cube, init_gl2, draw_2, shader_bind

from numpy import array, eye, zeros, float32, uint32, transpose
import time

from texture import load_texture
from shader import Shader, _init_gl
from camera import Camera
from voxel_renderer import VoxelRenderer
from chunk import Chunk
from mesh import Mesh
from chunks import Chunks

def main():
	display_size = (800, 600)
	
	w = Window.init(display_size)
	e = Events.init()
	
	#_init_gl("res/shaders/sh2.vert", "res/shaders/sh2.frag")

	shader = Shader("res/shaders/sh2.vert", "res/shaders/sh2.frag")
	if shader is None:
		w.terminate()
		exit()

	texture = load_texture("res/block.png")
	if texture is None:
		w.terminate()
		exit()


	renderer = VoxelRenderer.init()#1024*1024*8)
	#chunk = Chunk(0,0,0)

	#mesh = Mesh(vertices, 6, array([3,2,1]))
	#mesh = renderer.render(chunk)


	chunks = Chunks.init(2,2,2)
	#print("chunks after init=",chunks.chunks)
	meshes = zeros(chunks.volume, dtype=object)

	#closes[27]
	#for i in range(chunks.volume):
		#chunk = chunks.chunks[i]
		#print("KKK=",i,"[",chunk,"]")
		#if chunk.modified == False:
		#	continue
		#chunk.modified = False
		#if not (meshes[i] is None):
		#meshes[i] = None
		#closes = [None] * 27
		#for j in range(chunks.volume):
		#	other = chunks.chunks[j]

		#	ox = other.x - chunk.x
		#	oy = other.y - chunk.y
		#	oz = other.z - chunk.z

		#	if (abs(ox) > 1 or abs(oy) > 1 or abs(oz) > 1):
		#		continue

		#	ox += 1
		#	oy += 1
		#	oz += 1
		#	closes[(oy * 3 + oz) * 3 + ox] = other

		#mesh = renderer.render(chunk)# (const Chunk**)closes);
		#meshes[i] = mesh


	cam = Camera.init(vec3(64,140,110), radians(70))

	#model = translate(mat4(1.0), vec3(1, 0, 0))
	#model = transpose(array(model))
	
	#projview = cam.get_m_proj_view()
	#print(projview, "\n")

	last_time = pg.time.get_ticks()
	del_time = 0.0
	speed = 0.02
	#FPS = 30
	#wait_time = int(1000/FPS) 

	camX = 0.0
	camY = 0.0
	clock = pg.time.Clock()
	while w.going:
		cur_time = pg.time.get_ticks()
		del_time = cur_time - last_time
		last_time = cur_time

		if e.j_pressed(pg.K_ESCAPE) or e.quit:
			w.going = False

		#if (e.j_pressed(pg.K_TAB)):
		#	e.toogleCursor()
		e._cursor_locked = False
		GL.glClearColor(0.5,0.5,0.5,1)
		if e.clicked(1):
			GL.glClearColor(0.3, 0.3, 0.3, 1)
			e._cursor_locked = True

		#if e.j_clicked(3):
		#	GL.glClearColor(0.5, 0.5, 0.5, 1)

		if e.pressed(pg.K_w):
			cam.pos += cam.front * del_time * speed
			#print("w")

		if e.pressed(pg.K_s):
			cam.pos -= cam.front * del_time * speed
			#print("S")


		if e.pressed(pg.K_a):
			cam.pos -= cam.right * del_time * speed
			#print("A")

		if e.pressed(pg.K_d):
			cam.pos += cam.right * del_time * speed
			#print("D")
			
		if e.pressed(pg.K_q):
			cam.pos -= cam.up * del_time * speed
			#print("Q")

		if e.pressed(pg.K_z):
			cam.pos += cam.up * del_time * speed
			#print("Z")	

		if e._cursor_locked:
			camY += -e.deltaY / w.display_size[1] * 4
			camX += -e.deltaX / w.display_size[0] * 4
			if (camY < -radians(89.0)):
				camY = -radians(89.0)
			if (camY > radians(89.0)):
				camY = radians(89.0)
			cam.rotation = mat4(1.0)
			cam.rotate(camY, camX, 0)
			projview = cam.get_m_proj_view()
			#pg.mouse.set_pos(w.display_size[0]/2, w.display_size[1]/2)


		for i in range(chunks.volume):
			chunk = chunks.chunks[i]
			if chunk.modified == False:
				continue
			chunk.modified = False
			if not (meshes[i] is None):
				meshes[i] = None
			mesh = renderer.render(chunk)
			meshes[i] = mesh
			print("load blocks ",int((i + 1) * 100 / chunks.volume),"%")

		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

		shader.use()

		#shader.uniform_matrix("model", model)
		
		shader.uniform_matrix("projview", cam.get_m_proj_view())
		#shader.bind()
		texture.bind()


		for i in range(chunks.volume):
			
			chunk = chunks.chunks[i]
			mesh = meshes[i]
			vec = vec3(chunk.x*65+1.0, chunk.y*65+1.0, chunk.z*65+1.0)
			#print("vec=", vec)
			model = translate(mat4(1.0), vec)
			model = transpose(array(model))
			shader.uniform_matrix("model", model)
			mesh.draw()#GL_TRIANGLES);

		#mesh.draw()#GL.GL_TRIANGLES)
		#shader.draw()
		w.flip()
		#pg.time.wait(wait_time)
		e.update()
	w.terminate()

if __name__ == "__main__":
	main()
