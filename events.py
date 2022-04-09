from re import match
from unittest import case

import pygame as pg

from numpy import zeros

from window import Window

from camera import Camera


class Events:
	events = None
	MOUSE_BUTTON = 1024

	@classmethod
	def init(cls):
		if Events.events is None:
			Events.events = Events()
		return Events.events

	def cursor_position_action(self, pos):
		xpos, ypos = pos
		if self._cursor_locked:
			self.deltaX += (xpos - self.x)
			self.deltaY += (ypos - self.y)
		else:
			self._cursor_started = True
		self.x = xpos
		self.y = ypos

	def mouse_button_action(self, button, action):
		if action == pg.MOUSEBUTTONDOWN:
			self._keys[Events.MOUSE_BUTTON + button] = 1
			self._frames[Events.MOUSE_BUTTON + button] = self._current
		elif action == pg.MOUSEBUTTONUP:
			self._keys[Events.MOUSE_BUTTON + button] = 0
			self._frames[Events.MOUSE_BUTTON + button] = self._current

	def key_action(self, key, action):
		if key>1032:
			key -= 1073741324
		if action == pg.KEYDOWN:
			self._keys[key] = 1
			if self._frames[key] == 0:
				self._frames[key] = self._current
				print(key, self._frames[key], self._current)
		elif action == pg.KEYUP:
			self._keys[key] = 0
			self._frames[key] = 0

	def __init__(self):
		self._keys = zeros(1032)
		self._frames = zeros(1032)
		self._current = 0
		self.deltaX = 0.0
		self.deltaY = 0.0
		self.x = 0.0
		self.y = 0.0
		self._cursor_locked = False
		self._cursor_started = False
		self.resize = False
		self.size = Window.window.display_size

	def pressed(self, keycode):
		if keycode < 0 or keycode >= Events.MOUSE_BUTTON:
			return False
		return bool(self._keys[keycode])

	def j_pressed(self, keycode):
		if keycode < 0 or keycode >= Events.MOUSE_BUTTON:
			return False
		return bool(bool(self._keys[keycode]) and bool(self._frames[keycode] == self._current))

	def clicked(self, button):
		index = Events.MOUSE_BUTTON + button
		return bool(self._keys[index])

	def j_clicked(self, button):
		index = Events.MOUSE_BUTTON + button
		return bool(self._keys[index] and self._frames[index] == self._current)

	def toogleCursor(self):
		pg.mouse.set_visible(self._cursor_locked)
		self._cursor_locked = not self._cursor_locked
		#Window::setCursorMode(_cursor_locked ? GLFW_CURSOR_DISABLED : GLFW_CURSOR_NORMAL);


	def update(self):
		self._current += 1
		self.deltaX = 0.0
		self.deltaY = 0.0
		events = pg.event.get()
		for event in events:
			if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
				self.key_action(event.key, event.type)
			elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
				self.mouse_button_action(event.button, event.type)
			elif event.type == pg.MOUSEMOTION:
				self.cursor_position_action(pg.mouse.get_pos())
			elif event.type == pg.QUIT:
				self.key_action(pg.KEYDOWN, pg.K_ESCAPE)
			elif event.type == pg.VIDEORESIZE:
				self.size = event.size
				self.resize = True


			'''
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
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