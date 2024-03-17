import numpy
import glm
import pygame as pg
import pywavefront

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
        self.texture = self.gen_texture(path='textures/sus.png')
        self.on_init()

    def gen_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data = pg.image.tostring(texture, 'RGB'))
        return texture
    
    def on_init(self):

        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.ambient'].write(self.app.light.ambient)
        self.shader_program['light.diffuse'].write(self.app.light.diffuse)
        self.shader_program['light.specular'].write(self.app.light.specular)

        self.shader_program['u_txt_0'] = 0
        self.texture.use()

        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def get_md_matrix(self):
        m_model = glm.mat4()
        return m_model

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f', 'in_texcoord_0', 'in_normal',  'in_position')])
        return vao
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.tk, glm.vec3(0.5, 1, 0))
        self.shader_program['m_model'].write(m_model)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['camPos'].write(self.app.camera.position)

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

        normals = [6*(0,0,1),6*(1,0,0),6*(0,0,-1),6*(-1,0,0),6*(0,1,0),6*(0,-1,0),]

        normals = numpy.array(normals, dtype = 'f4').reshape(36, 3)

        vertex_data = numpy.hstack([normals, vertex_data])
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
    

class Human(Cube):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        self.meshes = self.load_meshes('objects/14-girl-obj/girl OBJ.obj')
        self.vao = self.get_vao()
        
    def get_vbo(self):
        vertex_data = self.get_vertex()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def load_meshes(self, obj_file_path):
        # Load the OBJ file
        scene = pywavefront.Wavefront(obj_file_path, collect_faces=True)
        meshes = []
        for material_name, material in scene.materials.items():
            # Assuming material contains a path to the texture
            texture_path = material.texture.file_name
            texture = self.gen_texture_hm(texture_path)
            
            # Collect vertex data for this part
            vertices = numpy.array(material.vertices, dtype='f4')
            
            # Append mesh information, including its texture and vertices
            meshes.append({
                'texture': texture,
                'vertices': vertices,
                'vertex_count': len(vertices) // 8  # 8 = number of floats per vertex
            })
        return meshes

    def gen_texture_hm(self, fn):
        # Load and convert the texture
        p = "objects/14-girl-obj/tEXTURE/" + fn
        texture = pg.image.load(p).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture_data = pg.image.tostring(texture, 'RGB')
        texture_id = self.ctx.texture(size=texture.get_size(), components=3, data=texture_data)
        return texture_id
    
    def render(self):
        self.update()  # Update transformations and other uniforms
        
        # Assuming your shader program is already correctly set up and used:
        # For each mesh part in the human model
        for mesh in self.meshes:
            # Bind the texture specific to this mesh part
            mesh['texture'].use(location=0)  # Adjust if your method or texture unit differs
            # Create a temporary VAO for this mesh part if you haven't already
            # This assumes each mesh part has its own vertex data format and needs its own VAO
            # Note: Ideally, you should create these VAOs ahead of time, not in the render loop
            self.vao = self.ctx.vertex_array(self.shader_program, [(self.ctx.buffer(mesh['vertices']), self.format, *self.attribs)])
            
            # Bind the VAO
            self.vao.render()
            
            # Delete the temporary VAO to clean up resources
            # Note: This is inefficient if done every frame. Ideally, maintain and reuse VAOs instead.
            del self.vao

    def update(self):
        m_model = glm.rotate(self.m_model, self.app.tk, glm.vec3(0, 0.5, 0))
        self.shader_program['m_model'].write(m_model)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['camPos'].write(self.app.camera.position)
    
    
    def get_vertex(self):
        objs = pywavefront.Wavefront('objects/14-girl-obj/girl OBJ.obj', collect_faces=True)
        # Convert all vertices for all meshes into a single flat list
        vertices = []
        for name, material in objs.materials.items():
            vertices.extend(material.vertices)
        return numpy.array(vertices, dtype='f4')
    
