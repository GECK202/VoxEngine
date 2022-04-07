#version 150
in vec4 vertex_color_out;  // vertex colour from vertex shader
out vec4 fragColor;
void main()
{
	fragColor = vertex_color_out;
}