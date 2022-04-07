#version 330 core

layout (location = 0) in vec3 vertex_position;

out vec4   a_color; 

void main() {
  a_color = vec4((0.5 - vertex_position), 1.0);
  gl_Position = vec4(vertex_position, 1.0);
}