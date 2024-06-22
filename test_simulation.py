from math import isclose
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class State:
    '''
    state structure
    state = {
        name or count of cell : {
            points of this cell: {x, y},
            property of this cell: {aim, color, is_find_aim, is_negative_gravity, is_zombie, is_run_away, speed,
                }
            }
    }
    '''

    count = 0
    do_onse = True
    __slots__ = ('aims', 'state')

    def __init__(self) -> None:
        self.state = {}
        self.aims = {
            'new_aims': {0: [90, 1], 1: [10, 50]},
            'old_aims': {0: [90, 1], 1: [10, 50]}
        }

    # add object to state (for work with him)
    def _add_object_to_dictionary(self, ob):
        self.state[State.count] = ob
        self.state[State.count]['points'] = (
            random.randint(0, 1), (random.randint(0, 1)))
        self.state[State.count]['props']['speed'] = (
            float(f'0.{random.randint(3,9)}'), float(f'0.{random.randint(3,9)}'))
        self.state[State.count]['props']['color'] = [
            1, float(f'0.{random.randint(1,1)}'), 1]
        # count for cell identity
        State.count += 1

    def _show_object(self, ob, color):
        glPointSize(8)
        glBegin(GL_POINTS)
        glColor3f(*color)
        glVertex2f(ob[0]/100, ob[1]/100)
        glEnd()

    # setup new Cell
    def create_new_object(self):
        new_object = Cell(0, 0)
        new_object.init_cell(self)

    def init_aim_in_object(self, name, is_zomb=False, coord=None):
        is_find_aim = self.state[name]['props']['is_find_aim']

        if self.state[name]['props']['is_run_away']:
            if coord != None:
                self.state[name]['props']['aim'][0] = coord[0]
                self.state[name]['props']['aim'][1] = coord[1]

        elif coord == None and not self.state[name]['props']['is_zombie'] and not is_find_aim:
            self.state[name]['props']['aim'][0] = self.aims['new_aims'][self.state[name]
                                                                        ['props']['aim_count']][0]
            self.state[name]['props']['aim'][1] = self.aims['new_aims'][self.state[name]
                                                                        ['props']['aim_count']][1]
            self.state[name]['props']['is_find_aim'] = True

        elif is_zomb:
            self.state[name]['props']['aim'][0] = coord[0]
            self.state[name]['props']['aim'][1] = coord[1]

    # main

    def update_object_position(self, name):
        # initialization
        gravity = self.state[name]['props']['is_negative_gravity']
        speed_x = self.state[name]['props']['speed'][0]
        speed_y = self.state[name]['props']['speed'][1]
        new_x = self.state[name]['points'][0]
        new_y = self.state[name]['points'][1]

        # update old position (for collision)
        self.state[name]['old_points'] = (new_x, new_y)

        # update old aims
        self.aims['old_aims'][0] = self.aims['new_aims'][0]
        self.aims['old_aims'][1] = self.aims['new_aims'][1]
        # drop points in objсet in order to count them to determine the aim
        # что то с плавностью делает !!!!!!!!!!!!!!!!!
        self.init_aim_in_object(name)
        self.find_nearest_aim(name)

        # setup new aim
        # aim = self.aims['new_aims'][0]
        aim = self.state[name]['props']['aim'][0:2]

        old_x = new_x
        old_y = new_y

        # border
        if new_x < 0:
            new_x = 59
            aim[0] = 50
            self.state[name]['props']['aim'][0] = 50
        if new_y < 0:
            new_y = 50
            aim[1] = 59
            self.state[name]['props']['aim'][1] = 59
        if new_x > 100:
            new_x = 59.0
            aim[0] = 50
            self.state[name]['props']['aim'][0] = 50
        if new_y > 100:
            new_y = 50.0
            aim[1] = 59
            self.state[name]['props']['aim'][1] = 59

        # basic movement logic
        if new_x < aim[0]:
            new_x += speed_x
        if new_x > aim[0]:
            new_x -= speed_x
        if new_y < aim[1] and (False == (isclose(new_y, aim[1], rel_tol=0.001))):
            new_y += speed_y
        if new_y > aim[1] and (False == (isclose(new_y, aim[1], rel_tol=0.001))):
            new_y -= speed_y

        # if cell stuck
        if old_x == new_x:
            new_x += .01
        if old_y == new_y:
            new_y += .01
        # collision check
        self.collision(name)
        # setup new points to state
        self.state[name]['points'] = (new_x, new_y)

        # cheack to achieve the aim
        if (isclose(new_x, aim[0], rel_tol=0.1)) and (isclose(new_y, aim[1], rel_tol=0.1)) and not self.state[name]['props']['is_zombie'] and not self.state[name]['props']['is_find_aim']:
            self.aims['new_aims'][self.state[name]['props']['aim_count']] = [
                random.randint(0, 99), random.randint(0, 99)]
            if 1 == 1:
                if State.do_onse:
                    self.state[name]['props']['color'] = [0, 1, 0]
                    self.state[name]['props']['is_zombie'] = True
                    State.do_onse = False

        self._show_object(self.state[name]['points'],
                          self.state[name]['props']['color'])

    def collision(self, name):
        state = self.show_state()
        reaction_force = 0.1
        accuracy = 0.01
        name_gravity = self.state[name]['props']['is_negative_gravity']

        def case_variation_handling(is_x_close, is_y_close):
            ''' 
             taking into account different situations
             1 if one negative another negative too
             2 if one positive another positive too
             3 if one positive another negtive
             4 if one negative another positive
            '''

            if is_x_close and is_y_close and ob_gravity and name_gravity:
                self.state[name]['points'] = (
                    self.state[name]['old_points'][0] - reaction_force, self.state[name]['old_points'][1] - reaction_force)
                self.state[ob]['points'] = (
                    self.state[ob]['old_points'][0] - reaction_force, self.state[ob]['old_points'][1] - reaction_force)

            if is_x_close and is_y_close and ob_gravity == False and name_gravity == False:
                self.state[name]['points'] = (
                    self.state[name]['old_points'][0] + reaction_force, self.state[name]['old_points'][1] + reaction_force)
                self.state[ob]['points'] = (
                    self.state[ob]['old_points'][0] + reaction_force, self.state[ob]['old_points'][1] + reaction_force)

            if is_x_close and is_y_close and ob_gravity == False and name_gravity:
                self.state[name]['points'] = (
                    self.state[name]['old_points'][0] + reaction_force, self.state[name]['old_points'][1] + reaction_force)
                self.state[ob]['points'] = (
                    self.state[ob]['old_points'][0] - reaction_force, self.state[ob]['old_points'][1] - reaction_force)

            if is_x_close and is_y_close and ob_gravity and name_gravity == False:
                self.state[name]['points'] = (
                    self.state[name]['old_points'][0] - reaction_force, self.state[name]['old_points'][1] - reaction_force)
                self.state[ob]['points'] = (
                    self.state[ob]['old_points'][0] + reaction_force, self.state[ob]['old_points'][1] + reaction_force)

        for ob in state:
            ob_gravity = self.state[ob]['props']['is_negative_gravity']
            is_x_close = isclose(
                state[name]['points'][0], state[ob]['points'][0], rel_tol=accuracy)
            is_y_close = isclose(
                state[name]['points'][1], state[ob]['points'][1], rel_tol=accuracy)
            case_variation_handling(is_x_close, is_y_close)

    def find_nearest_aim(self, name):
        zomb = None
        is_run_away = False

        def is_zombie_near():
            maximum_distance = [10, 10]
            for ob in self.state:
                if self.state[ob]['props']['is_zombie']:
                    x = self.state[name]['points'][0]
                    y = self.state[name]['points'][1]
                    x_zomb = self.state[ob]['points'][0]
                    y_zomb = self.state[ob]['points'][1]
                    if y <= y_zomb and x >= x_zomb:
                        if [x + x_zomb, y - y_zomb] <= maximum_distance:
                            self.state[name]['props']['is_run_away'] = True
                            return ob

                    if y <= y_zomb and x <= x_zomb:
                        if [x + x_zomb, y + y_zomb] < maximum_distance:
                            self.state[name]['props']['is_run_away'] = True
                            return ob

                    if y >= y_zomb and x <= x_zomb:
                        if [x - x_zomb, y + y_zomb] < maximum_distance:
                            self.state[name]['props']['is_run_away'] = True
                            return ob

                    if y >= y_zomb and x >= x_zomb:
                        if [x - x_zomb, y - y_zomb] < maximum_distance:
                            self.state[name]['props']['is_run_away'] = True
                            return ob

            self.state[name]['props']['is_run_away'] = False

        if self.state[name]['props']['is_zombie'] == False:
            zomb = is_zombie_near()
            is_run_away = self.state[name]['props']['is_run_away']
            if is_run_away:
                x = self.state[name]['points'][0]
                y = self.state[name]['points'][1]
                x_zomb = self.state[zomb]['points'][0]
                y_zomb = self.state[zomb]['points'][1]

                if abs(x - x_zomb) <= 5:
                    x += 5
                else:
                    x -= 5
                if abs(y - y_zomb) <= 5:
                    y += 5
                else:
                    y -= 5

                coord = [x, y]
                self.init_aim_in_object(name=name, coord=coord)

            if self.state[name]['props']['is_find_aim'] and not is_run_away:
                if self.aims['old_aims'][self.state[name]['props']['aim_count']] == self.aims['new_aims'][self.state[name]['props']['aim_count']]:
                    self.state[name]['props']['is_find_aim'] = False

            if self.state[name]['props']['is_find_aim'] == False and not is_run_away:
                first = self.aims['new_aims'][0]
                second = self.aims['new_aims'][1]
                x = self.state[name]['points'][0]
                y = self.state[name]['points'][1]
                if [first[0] - x, first[1] - y] < [second[0] - x, second[1] - y]:
                    self.state[name]['props']['aim'] = [*first]
                    self.state[name]['props']['aim_count'] = 0
                else:
                    self.state[name]['props']['aim'] = [*second]
                    self.state[name]['props']['aim_count'] = 1

        elif self.state[name]['props']['is_zombie']:
            x = self.state[name]['points'][0]
            y = self.state[name]['points'][1]
            min_points = [self.state[name]['props']['aim']
                          [0], self.state[name]['props']['aim'][1]]
            for ob in self.state:
                # for that if object dont pic himself
                if name != ob:
                    if min_points > [self.state[ob]['points'][0], self.state[ob]['points'][1]]:
                        min_points = [self.state[ob]['points']
                                      [0], self.state[ob]['points'][1]]

            # ob = name-1
            # if name != ob:
            #     if min_points > [self.state[ob]['points'][0], self.state[ob]['points'][1]]:
            #         min_points = [self.state[ob]['points'][0], self.state[ob]['points'][1]]
            self.init_aim_in_object(name=name, is_zomb=True, coord=min_points)

    def zombie_logic(self, name):
        # this method change basic Cell logic that create new aim in the form of cells
        # who has these targets named zombies
        pass

    def show_state(self):
        return self.state


class Cell(State):
    # Main character class
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'cell - {State.count}'

    def init_cell(self, state_instance):
        state_instance._add_object_to_dictionary(
            {
                'points': (self.x, self.y),
                'old_points': (self.x, self.y),
                'props': self.set_propirties(),
            }
        )

    def set_propirties(self):
        return {
            'aim': [1, 11],
            'color': None,
            'aim_count': 0,
            'is_find_aim': False,
            'is_negative_gravity': True,
            'speed': None,
            'is_zombie': False,
            'is_run_away': False,
        }

    # not yet thought of useful in the future
    def change_propirties(self):
        pass


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


class Game:
    def __init__(self) -> None:
        self.window = Window([600, 600])
        self.state = State()

    def main(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        print("D key pressed!")

            self.window.clear()
            for ob in self.state.show_state():
                self.state.update_object_position(ob)
            self.window.flip()
            self.window.wait(10)


game = Game()
for i in range(0, 100):
    game.state.create_new_object()
game.main()
