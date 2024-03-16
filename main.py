import pygame as pg
import moderngl as mgl
import sys

class GraphicsEngine:
    def __init__(self, win_size = (1600, 900)):
        pg.init()

        self.WIN_SIZE = win_size
        
        #  using v3.3 for opengl
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_get_attribute(pg.GL_CONTEXT_PROFILE_MASK , pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.WIN_SIZE, flags = pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.timer = pg.time.Clock()

    def render(self):
        self.ctx.clear(color=(1,1,1))
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.key == pg.K_ESCAPE and event.type == pg.KEYDOWN):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.render()
            self.timer.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    print("Now running")
    app.run
    