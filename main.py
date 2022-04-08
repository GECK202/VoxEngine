import ctypes

import pygame as pg
from window import Window
from events import Events
from shader import Shader

import OpenGL.GL as GL

import glm
#from ogl3 import init_gl_rot, draw_cube, init_gl2, draw_2, shader_bind

from numpy import array, eye, zeros, float32, uint32

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

	cam = Camera.init(glm.vec3(0,0,1))

	model = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, 0.5))
	model = array(model)

	projview = cam.get_m_proj_view()
	print(projview, "\n")
	while w.going:
		e.update()
		if e.j_pressed(pg.K_ESCAPE):
			w.going = False
		if e.j_clicked(1):
			GL.glClearColor(0.3, 0.3, 0.3, 1)
		if e.j_clicked(3):
			GL.glClearColor(0.5, 0.5, 0.5, 1)
		if e.pressed(pg.K_w):
			cam.pos.z -= 0.016
			projview = cam.get_m_proj_view()
		if e.pressed(pg.K_s):
			cam.pos.z += 0.016
			projview = cam.get_m_proj_view()

		GL.glClear(GL.GL_COLOR_BUFFER_BIT)

		#shader.use()
		shader.uniform_matrix("model", model)
		#shader.use()
		
		shader.uniform_matrix("projview", projview)
		shader.bind()
		texture.bind()

		shader.draw()
		w.flip()
	w.terminate()


if __name__ == "__main__":
	main()
