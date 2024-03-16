import numpy

class Tri:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')

    def get_vertex(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = numpy.array(vertex_data, dtype='f4')
        return vertex_data
    
    def get_vbo(self):
        vertex_data = self.get_vertex()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        prog = self.ctx.program(vertex_shader = vertex_shader, fragment_shader=fragment_shader)
        return prog