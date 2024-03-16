import numpy

class Tri:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

    def get_vertex(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = numpy.array(vertex_data, dtype='f4')
        return vertex_data
    
    def get_vbo(self):
        vertex_data = self.get_vertex()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    