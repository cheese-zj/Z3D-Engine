import glm
import pygame as pg

FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENS = 0.15

class Camera:
    def __init__(self, app, pos = (0, 0, 4), yaw = -90, pitch = 0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(2,3,3)
        self.up = glm.vec3(0,1,0)
        self.forward = glm.vec3(0,0,-1)
        self.flat = glm.vec3(1,0,0)
        self.yaw = yaw
        self.pitch = pitch
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward , self.up )

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def move(self): 
        v = SPEED * self.app.dtk
        k = pg.key.get_pressed()
        if k[pg.K_w]: self.position += self.forward * v
        if k[pg.K_s]: self.position -= self.forward * v
        if k[pg.K_d]: self.position += self.flat * v
        if k[pg.K_a]: self.position -= self.flat * v
        if k[pg.K_SPACE]: self.position += self.up * v
        if k[pg.K_LCTRL]: self.position -= self.up * v

    def rotate(self):
        rx, ry = pg.mouse.get_rel()
        if pg.mouse.get_pressed()[0]:
            self.yaw += rx * SENS
            self.pitch -= ry * SENS
            self.pitch = max(-89, min(89, self.pitch))  # limiting the angel to 89 to prevent fliping the whole camera

    def update_cam_vec(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.flat = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0) ))
        self.up = glm.normalize(glm.cross(self.flat, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_cam_vec()
        self.m_view = self.get_view_matrix()

