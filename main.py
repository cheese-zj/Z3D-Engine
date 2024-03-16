import pygame as pg
import moderngl as gl
import sys

class GraphicsEngine:
    def __init__(self, win_size = (1200, 720)):
        pg.init()

        self.WIN_SIZE = win_size
        
        #  using v3.3 for opengl
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK , pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.WIN_SIZE, flags = pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = gl.create_context()

        self.timer = pg.time.Clock()

    def render(self):
        self.ctx.clear(color=(1,1,1))
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def run(self):
        print("Starting run loop")
        while True:
            self.check_events()
            self.render()
            self.timer.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    # print("Now running")
    app.run()
    