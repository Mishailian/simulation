import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from window import Window
from state import State
from static import Static

class Game:
    def __init__(self) -> None:
        self.static = Static()
        self.state = State()
        self.clock = pygame.time.Clock()
        self.hero_speed = self.static.get_hero_data()['hero_config']['speed']
        self.resolution = self.static.get_window_data()['resolution']
        self.window = Window(self.resolution)
        self.fps = self.static.get_game_data()['fps']
        self.count_of_objects = self.static.get_game_data()['count_of_objects']


    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            delta_time = self.clock.get_time() / 1000.0 # Время, прошедшее с последнего кадра, в секундах

            if keys[pygame.K_l]:
                print("D key pressed!")
            if keys[pygame.K_w]:
                self.state.hero_controls(0,delta_time * self.hero_speed)
            if keys[pygame.K_s]:
                self.state.hero_controls(0,delta_time * -self.hero_speed)
            if keys[pygame.K_a]:
                self.state.hero_controls(delta_time * -self.hero_speed,0)
            if keys[pygame.K_d]:
                self.state.hero_controls(delta_time * self.hero_speed,0)

            self.window.clear()
            for ob in self.state.show_state():
                self.state.update_object_position(ob)

            self.window.flip()
            self.window.wait(10)
            # lock 60 FPS
            self.clock.tick(self.fps)  


game = Game()
game.state.create_hero()
for i in range(0, game.count_of_objects):
    game.state.create_new_object()
game.main()
