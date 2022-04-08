import ctypes

import pygame as pg
from window import flip, terminate, Window
from events import Events
from shader import Shader

import OpenGL.GL as GL
from ogl3 import init_gl_rot, draw_cube, init_gl2, draw_2, shader_bind

from numpy import array, eye, zeros, float32, uint32

from texture import load_texture

def main():
	display_size = (600, 600)
	Window.init(display_size)
	Events.init()
	#p = init_gl_rot(display_size)
	p = init_gl2()

	texture = load_texture("res/block.png")
	if texture is None:
		terminate()
		exit()


	GL.glClearColor(0.5, 0.5, 0.5, 1)
	GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
	GL.glEnable(GL.GL_BLEND)

	while Window.window.going:
		Events.events.update()
		if Events.events.j_pressed(pg.K_ESCAPE):
			Window.window.going = False
		if Events.events.j_clicked(1):
			GL.glClearColor(1, 0, 0, 1)
		if Events.events.j_clicked(3):
			GL.glClearColor(0.5, 0.5, 0.5, 1)

		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
		#draw_cube(p)
		shader_bind(p)
		texture.bind()


		draw_2()
		flip()
	terminate()


if __name__ == "__main__":
	main()

'''
	VAO = GL.glGenVertexArrays(1)
	VBO = GL.glGenBuffers(1)

	GL.glBindVertexArray(VAO)
	GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
	GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

	stride = vertices.strides[0]
	offset = ctypes.c_void_p(0)

	GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 3 * , offset)
	GL.glEnableVertexAttribArray(0)

	GL.glBindVertexArray(0)
'''