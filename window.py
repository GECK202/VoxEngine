import pygame as pg
import OpenGL.GL as GL


class Window:
	window = None
	@classmethod
	def init(cls, display_size):
		if Window.window is None:
			Window.window = Window(display_size)
		return Window.window

	def __init__(self, display_size):
		pg.init()
		gl_version = (4, 0)  # GL Version number (Major, Minor)

		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, gl_version[1])
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

		self.fs = False  # start in windowed mode
		self.going = True
		self.display_size = display_size
		pg.display.set_mode(display_size, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
		
		GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
		#GL.glEnable(GL.GL_BLEND)

		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glEnable(GL.GL_CULL_FACE)
		GL.glEnable(GL.GL_BLEND)

		GL.glClearColor(0.5, 0.5, 0.5, 1)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
		pg.display.flip()
		GL.glClearColor(0.5, 0.5, 0.5, 1)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)

	def flip(self):
		pg.display.flip()
		pg.time.wait(10)


	def terminate(self):
		pg.quit()

'''
	def update(self):
		events = pg.event.get()
		for event in events:
			if event.type == pg.QUIT or (
					event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
			):
				self.going = False

			elif event.type == pg.KEYDOWN and event.key == pg.K_f:
				if not self.fs:
					print("Changing to FULLSCREEN")
					pg.display.set_mode(self.display_size, pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
				else:
					print("Changing to windowed mode")
					pg.display.set_mode(self.display_size, pg.OPENGL | pg.DOUBLEBUF)
				self.fs = not self.fs
'''