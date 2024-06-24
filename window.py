import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
class Window:
    # setup all props for the screan
    def __init__(self, display_size) -> None:
        self.display_size = display_size
        pygame.init()
        pygame.display.set_mode(self.display_size, DOUBLEBUF | OPENGL)
        gluOrtho2D(0, 1, 0, 1)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def flip(self):
        pygame.display.flip()

    def wait(self, time):
        pygame.time.wait(time)

