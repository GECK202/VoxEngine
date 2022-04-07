from PIL import Image
import numpy as np
import OpenGL.GL as GL

def load_im():
    im_frame = Image.open("res/block.png")
    np_frame = np.array(im_frame.getdata())
    print(np_frame)

def create_texture():
    texture_map = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_map)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D , GL.GL_TEXTURE_MAG_FILTER , GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D , GL.GL_TEXTURE_WRAP_S , GL.GL_CLAMP_TO_BORDER)
    GL.glTexParameteri(GL.GL_TEXTURE_2D , GL.GL_TEXTURE_WRAP_T , GL.GL_CLAMP_TO_BORDER)
    
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA , fbo_width, fbo_height, 0, GL.GL_RGBA , GL.GL_UNSIGNED_BYTE , None)
    glBindTexture (GL_TEXTURE_2D, 0)