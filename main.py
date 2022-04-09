import ctypes

import pygame as pg
from window import Window
from events import Events
from shader import Shader

import OpenGL.GL as GL

from glm import vec3, vec4, mat4, radians, translate
#from ogl3 import init_gl_rot, draw_cube, init_gl2, draw_2, shader_bind

from numpy import array, eye, zeros, float32, uint32, transpose

from texture import load_texture
from shader import Shader
from camera import Camera

def main():
	display_size = (600, 600)
	
	w = Window.init(display_size)
	e = Events.init()
	
	shader = Shader("res/shaders/sh2.vert", "res/shaders/sh2.frag")
	if shader is None:
		w.terminate()
		exit()

	texture = load_texture("res/block2.png")
	if texture is None:
		w.terminate()
		exit()

	cam = Camera.init(vec3(0,0,1), radians(70))

	model = translate(mat4(1.0), vec3(0.5, 0, 0))
	model = transpose(array(model))
	
	projview = cam.get_m_proj_view()
	print(projview, "\n")

	last_time = pg.time.get_ticks()
	del_time = 0.0
	speed = 0.001
	FPS = 60
	wait_time = int(1000/FPS) 

	camX = 0.0
	camY = 0.0

	while w.going:
		cur_time = pg.time.get_ticks()
		del_time = cur_time - last_time
		last_time = cur_time

		if e.j_pressed(pg.K_ESCAPE):
			w.going = False

		if (e.j_pressed(pg.K_TAB)):
			e.toogleCursor()
		
		if e.j_clicked(1):
			GL.glClearColor(0.3, 0.3, 0.3, 1)

		if e.j_clicked(3):
			GL.glClearColor(0.5, 0.5, 0.5, 1)

		if e.pressed(pg.K_w):
			cam.pos += cam.front * del_time * speed
			projview = cam.get_m_proj_view()

		if e.pressed(pg.K_s):
			cam.pos -= cam.front * del_time * speed
			projview = cam.get_m_proj_view()

		if e.pressed(pg.K_a):
			cam.pos -= cam.right * del_time * speed
			projview = cam.get_m_proj_view()
			print(projview, "\n")

		if e.pressed(pg.K_d):
			cam.pos += cam.right * del_time * speed
			projview = cam.get_m_proj_view()
			print(projview, "\n")

		if e.resize:
			e.resize = False
			w.display_size = e.size
			projview = cam.get_m_proj_view()

		if e._cursor_locked:
			camY += -e.deltaY / w.display_size[1] * 2
			camX += -e.deltaX / w.display_size[1] * 2

			if (camY < -radians(89.0)):
				camY = -radians(89.0)
			if (camY > radians(89.0)):
				camY = radians(89.0)
			cam.rotation = mat4(1.0)
			cam.rotate(camY, camX, 0)

		GL.glClear(GL.GL_COLOR_BUFFER_BIT)

		#shader.use()
		shader.uniform_matrix("model", model)
		#shader.use()
		
		shader.uniform_matrix("projview", projview)
		shader.bind()
		texture.bind()

		shader.draw()
		w.flip()
		pg.time.wait(wait_time)
		e.update()
	w.terminate()


if __name__ == "__main__":
	main()
