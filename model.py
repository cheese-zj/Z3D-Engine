import numpy
import glm
import pygame

# class Tri:
#     def __init__(self, app):
#         self.app = app
#         self.ctx = app.ctx
#         self.vbo = self.get_vbo()
#         self.shader_program = self.get_shader_program('default')
#         self.vao = self.get_vao()
#         self.m_model = self.get_model_matrix()
#         self.on_init()

#     def get_model_matrix(self):
#         m_model = glm.mat4()
#         return m_model

#     def get_vao(self):
#         vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
#         return vao
    
#     def render(self):
#         self.vao.render()

#     def destroy(self):
#         self.vbo.release()
#         self.shader_program.release()
#         self.vao.release()


#     def get_vertex(self):
#         vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
#         vertex_data = numpy.array(vertex_data, dtype='f4')
#         return vertex_data
    
#     def get_vbo(self):
#         vertex_data = self.get_vertex()
#         vbo = self.ctx.buffer(vertex_data)
#         return vbo
    
#     def get_shader_program(self, shader_name):
#         with open(f'shaders/{shader_name}.vert') as file:
#             vertex_shader = file.read()
#         with open(f'shaders/{shader_name}.frag') as file:
#             fragment_shader = file.read()

#         prog = self.ctx.program(vertex_shader = vertex_shader, fragment_shader=fragment_shader)
#         return prog
    
class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_md_matrix()
        self.on_init()

    def gen_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = self.ctx.texture(size=texture.get_size(), components=3, data = pygame.image.tostring(texture, 'RGB'))
        return texture
    
    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def get_md_matrix(self):
        m_model = glm.mat4()
        return m_model

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])
        return vao
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.tk, glm.vec3(0.5, 1, 0))
        self.shader_program['m_model'].write(m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    @staticmethod
    def get_data_cube(vertices, indices):
        data = [vertices[ind] for tri in indices for ind in tri]
        return numpy.array(data, dtype='f4')


    def get_vertex(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        
        vertex_data = self.get_data_cube(vertices, indices)
        
        texture_coord = [(0,0),(1,0),(1,1),(0,1)]
        texture_coord_indices = [(0, 2, 3), (0, 1, 2),
                                 (0, 2, 3), (0, 1, 2),
                                 (0, 1, 2), (2, 3, 0),
                                 (2, 3, 0), (2, 0, 1),
                                 (0, 2, 3), (0, 1, 2),
                                 (3, 1, 2), (3, 0, 1),]

        texture_coord_data = self.get_data_cube(texture_coord, texture_coord_indices)

        vertex_data = numpy.hstack([texture_coord_data, vertex_data])
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