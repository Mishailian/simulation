import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from cell import Cell
from aim_manager import AimManager
from movement_manager import Movement_manager
from border_manager import Border_manager
from collision_manager import Collision_manager
from static import Static

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
    count = 1
    do_onse = True
    __slots__ = ('state', 'static', 'aim_manager', 'movement_manager', 'border_manager', 'collision_manager')

    def __init__(self) -> None:
        self.aim_manager = AimManager()
        self.movement_manager = Movement_manager()
        self.border_manager = Border_manager()
        self.collision_manager = Collision_manager()
        self.static = Static()
        self.state = {}
        
    def show_state(self):
        return self.state
    
    # add object to state (for work with him)
    def _add_object_to_dictionary(self, ob, is_hero=False, hero_config={}):
        if is_hero:
            self.state[0] = ob
            self.state[0]['props']['color'] = self.static.get_hero_data()['hero_config']['color']
            self.state[0]['props']['size'] = self.static.get_hero_data()['hero_config']['size']
        else:
            self.state[State.count] = ob
            self.state[State.count]['points'] = (
                random.randint(0, 1), (random.randint(0, 1)))
            self.state[State.count]['props']['speed'] = (
                float(f'0.{random.randint(3,9)}'), float(f'0.{random.randint(3,9)}'))
            self.state[State.count]['props']['color'] = [
                1, float(f'0.{random.randint(1,1)}'), 1]
            # count for cell identity
            State.count += 1

    def _show_object(self, ob, color, size):
        glPointSize(size)
        glBegin(GL_POINTS)
        glColor3f(*color)
        glVertex2f(ob[0]/100, ob[1]/100)
        glEnd()

    # setup new Cell
    def create_new_object(self):
        new_object = Cell(0, 0)
        new_object.init_cell(self)

    def create_hero(self):
        new_object = Cell(50, 50)
        new_object.init_cell(self, True, self.static.get_hero_data()['hero_config'])
    
    # used in exports
    def compare_lists_by_sum(self, list1, list2):
        return sum(list1) <= sum(list2)
    
    def hero_controls(self, force_x, force_y):
        x = self.state[0]['points'][0]
        y = self.state[0]['points'][1]
        self.state[0]['points'] = (x+force_x, y+force_y)

   # main loop
    def update_object_position(self, name):
        # initialization
        if not self.state[name]['is_hero']:
            coords = self.state[name]['points']

            # update old position (for collision)
            self.state[name]['old_points'] = coords

            # drop points in objсet in order to count them to determine the aim
            self.aim_manager.init_aim_in_object(self, name)
            self.aim_manager.find_nearest_aim(self, name)

            # setup new aim
            aim = self.state[name]['props']['aim'][0:2]

            # border
            coords = self.border_manager.main(coords)

            # collision check
            self.collision_manager.collision(self,name)

            # basic movement logic
            coords = self.movement_manager.main(self.state[name], aim=aim, points=coords)

            # check aim achivement
            self.aim_manager.handle_aim_achievement(self, name=name, coords=coords, aim=aim)

            # это бы убрать куда то 
            if 1 == 1:
                if State.do_onse:
                    self.state[name]['props']['color'] = [0, 1, 0]
                    self.state[name]['props']['is_zombie'] = True
                    self.state[name]['props']['speed'] = [1, 1]
                    State.do_onse = False

        self._show_object(self.state[name]['points'],
                        self.state[name]['props']['color'],
                        self.state[name]['props']['size'])