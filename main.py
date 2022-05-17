
import pygame as pg
from window import Window
from events import Events

import OpenGL.GL as GL

from glm import vec3, vec4, mat4, radians, translate

from numpy import array, zeros, transpose

from texture import load_texture
from shader import Shader
from camera import Camera
from voxel_renderer import VoxelRenderer, render
from chunks import Chunks
from hmap import Hmap 
import time



CHUNK_W, CHUNK_H, CHUNK_D = 32,32,32
MAP_W, MAP_H, MAP_D = 5, 8, 5

CHUNK_W2, CHUNK_D2 = CHUNK_W / 2, CHUNK_D / 2

CV_W = ((MAP_W - 1) * CHUNK_W - MAP_W) // 2
CV_D = ((MAP_D - 1) * CHUNK_D - MAP_D) // 2

def main():
	display_size = (1280, 1024)

	w = Window.init(display_size)
	e = Events.init()

	shader = Shader("res/shaders/sh2.vert", "res/shaders/sh2.frag")
	if shader is None:
		w.terminate()
		exit()

	texture = load_texture("res/block.png")
	if texture is None:
		w.terminate()
		exit()

	#renderer = 
	VoxelRenderer.init()


	print("Start load map...")
	Hmap.init(MAP_W, MAP_H, MAP_D)
	print("End load map. OK.")

	print("Start create chunks...")
	chunks = Chunks.init(MAP_W, MAP_H, MAP_D)
	print("End create chunks. Ok.")
	meshes = zeros(chunks.volume, dtype=object)

	cam = Camera.init(vec3(CHUNK_W * MAP_W / 2, MAP_H * CHUNK_H/2, CHUNK_D * MAP_D / 2), radians(70))

	last_time = pg.time.get_ticks()
	speed = 0.02

	camX = 0.0
	camY = 0.0

	while w.going:
		cur_time = pg.time.get_ticks()
		del_time = cur_time - last_time
		last_time = cur_time

		if e.j_pressed(pg.K_ESCAPE) or e.quit:
			w.going = False

		e.cursor_locked = False
		GL.glClearColor(0.5, 0.5, 0.5, 1)
		if e.clicked(1):
			GL.glClearColor(0.3, 0.3, 0.3, 1)
			e.cursor_locked = True

		pos_change = False
		if e.pressed(pg.K_w):
			cam.pos += cam.front * del_time * speed
			pos_change = True

		if e.pressed(pg.K_s):
			cam.pos -= cam.front * del_time * speed
			pos_change = True

		if e.pressed(pg.K_a):
			cam.pos -= cam.right * del_time * speed
			pos_change = True

		if e.pressed(pg.K_d):
			cam.pos += cam.right * del_time * speed
			pos_change = True

		if e.pressed(pg.K_q):
			cam.pos -= cam.up * del_time * speed
			pos_change = True

		if e.pressed(pg.K_e):
			cam.pos += cam.up * del_time * speed
			pos_change = True

		if e.cursor_locked:
			camY += -e.deltaY / w.display_size[1] * 4
			camX += -e.deltaX / w.display_size[0] * 4
			if camY < -radians(89.0):
				camY = -radians(89.0)
			if camY > radians(89.0):
				camY = radians(89.0)
			cam.rotation = mat4(1.0)
			cam.rotate(camY, camX, 0)

		start_time = time.time()
		n = 0
		for i in range(chunks.volume):
			chunk = chunks.chunks[i]
			#if pos_change:
			#	mx = cam.pos[0] + CV_W
			#	mz = cam.pos[2] + CV_D
			#	if chunk.x < mx:
			#		chunk.x += MAP_W * CHUNK_W
			#		chunk.modified = True
			if not chunk.modified:
				continue
			
			n += 1
			chunk.modified = False
			chunk.full_up()
			chunks.chunks[i] = chunk
			if not (meshes[i] is None):
				meshes[i] = None
			mesh = render(chunk)
			meshes[i] = mesh
		if n > 0:
			delta = (time.time() - start_time)
			ps = delta / n
			print("Was modify", n, "chunks! - ", delta, " seconds, ", ps, "sec per chunk")
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

		shader.use()
		shader.uniform_matrix("projview", cam.get_m_proj_view())
		texture.bind()

		for i in range(chunks.volume):
			chunk = chunks.chunks[i]
			mesh = meshes[i]
			vec = vec3(chunk.x, chunk.y, chunk.z)
			model = translate(mat4(1.0), vec)
			model = transpose(array(model))
			shader.uniform_matrix("model", model)
			mesh.draw()
		#print("cycle")
		w.flip()
		e.update()
	w.terminate()

if __name__ == "__main__":
	main()
