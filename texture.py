from PIL import Image
import numpy as np
import OpenGL.GL as GL

def load_im(filename):
	image = Image.open(filename)
	return image

def create_texture(filename):
	im = load_im(filename)
	tex_id = GL.glGenTextures(1)
	GL.glBindTexture(GL.GL_TEXTURE_2D, tex_id)
	#GL.glPixelStorei(GL.GL_UNPACK_ALIGMENT, 1)
	im_data = np.array(im.getdata())
	GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA , im.size[0], im.size[1], 0, GL.GL_RGBA , GL.GL_UNSIGNED_BYTE , im_data)
	GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
	GL.glTexParameteri(GL.GL_TEXTURE_2D , GL.GL_TEXTURE_MAG_FILTER ,GL.GL_NEAREST)
	GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
	return tex_id, im.size[0], im.size[1]

class Texture:
	def __init__(self, p):
		self.id, self.width, self.height = p

	def bind(self):
		GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)

	def __del__(self):
		GL.glDeleteTextures(1, self.id)


def load_texture(filename):
	p = create_texture(filename)
	if p[0] == 0:
		print("file", filename, "will not be load!")
		return None
	return Texture(p)
