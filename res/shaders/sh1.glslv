#version 150
uniform mat4   model;
uniform mat4   view;
uniform mat4   projection;

uniform vec4   colour_mul;
uniform vec4   colour_add;

in vec4 vertex_colour;         // vertex colour in
in vec3 vertex_position;

out vec4   vertex_color_out;            // vertex colour out
void main()
{
	vertex_color_out = (colour_mul * vertex_colour) + colour_add;
	gl_Position = projection * view * model * vec4(vertex_position, 1.0);
}