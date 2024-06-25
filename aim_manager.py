import random
from math import isclose
from bot_manager import Bot_manager
from static import Static

class AimManager:
    def __init__(self):
        self.bot_manager = Bot_manager()
        self.static = Static()
        self.aims = {
            'new_aims': {0: [80, 1], 1: [10, 50]},
            'old_aims': {0: [80, 1], 1: [10, 50]}
        }
        self.min_border = self.static.get_borders_data()['min_border']
        self.max_border = self.static.get_borders_data()['max_border']
        self.min_aim_spawn_range = self.static.get_spawn_aim_range()['min']
        self.max_aim_spawn_range = self.static.get_spawn_aim_range()['max']
        self.vision_range = self.static.get_cell_data()['vision_range']
        self.run_away = self.static.get_cell_data()['run_away']
        self.run_away_range = self.static.get_cell_data()['run_away_range']

    def set_borders_aim(self, min_borders, max_border, aim):
        if aim < min_borders:
            return min_borders
        if aim > max_border:
            return max_border
        return aim

    def init_aim_in_object(self, obj, name, is_zomb=False, coord=None):

        # update old aims
        self.aims['old_aims'][0] = self.aims['new_aims'][0]
        self.aims['old_aims'][1] = self.aims['new_aims'][1]

        is_find_aim = obj.state[name]['props']['is_find_aim']

        if obj.state[name]['props']['is_run_away']:
            if coord != None:
                obj.state[name]['props']['aim'][0] = self.set_borders_aim(self.min_border, self.max_border, coord[0])
                obj.state[name]['props']['aim'][1] = self.set_borders_aim(self.min_border, self.max_border, coord[1])

        elif coord == None and not obj.state[name]['props']['is_zombie'] and not is_find_aim:
            obj.state[name]['props']['aim'][0] = self.aims['new_aims'][obj.state[name]
                                                                        ['props']['aim_count']][0]
            obj.state[name]['props']['aim'][1] = self.aims['new_aims'][obj.state[name]
                                                                        ['props']['aim_count']][1]
            obj.state[name]['props']['is_find_aim'] = True

        elif is_zomb:
            obj.state[name]['props']['aim'][0] = self.set_borders_aim(self.min_border + 1 , self.max_border - 1, coord[0])
            obj.state[name]['props']['aim'][1] = self.set_borders_aim(self.min_border + 1 , self.max_border - 1, coord[1])

    def update_position(self, obj):
        speed_x, speed_y = obj['props']['speed']
        new_x, new_y = obj['points']
        aim_x, aim_y = obj['props']['aim']
        
        if new_x < aim_x:
            new_x += speed_x
        if new_x > aim_x:
            new_x -= speed_x
        if new_y < aim_y and not isclose(new_y, aim_y, rel_tol=0.001):
            new_y += speed_y
        if new_y > aim_y and not isclose(new_y, aim_y, rel_tol=0.001):
            new_y -= speed_y
        
        return new_x, new_y
    
    def handle_aim_achievement(self, obj, name, coords, aim):
        
        if (isclose(coords[0], aim[0], rel_tol=0.1)) and (isclose(coords[1], aim[1], rel_tol=0.1)) and not obj.state[name]['props']['is_zombie'] and not obj.state[name]['props']['is_find_aim']:
            self.aims['new_aims'][obj.state[name]['props']['aim_count']] = [
                random.randint(self.min_aim_spawn_range, self.max_aim_spawn_range),
                random.randint(self.min_aim_spawn_range, self.max_aim_spawn_range)]

    def find_nearest_aim(self, obj, name):
            zomb = None
            is_run_away = False
            
            def is_zombie_near():
                for ob in obj.state:
                    if obj.state[ob]['props']['is_zombie']:
                        x = obj.state[name]['points'][0]
                        y = obj.state[name]['points'][1]
                        x_zomb = obj.state[ob]['points'][0]
                        y_zomb = obj.state[ob]['points'][1]
                        res = [abs(x - x_zomb), abs(y - y_zomb)]

                        if obj.compare_lists_by_sum(res, self.vision_range):
                            obj.state[name]['props']['is_run_away'] = True
                            return ob

                obj.state[name]['props']['is_run_away'] = False

            if not obj.state[name]['props']['is_zombie']:
                zomb = is_zombie_near()
                # zomb = False
                is_run_away = obj.state[name]['props']['is_run_away']
                if is_run_away :
                    x = obj.state[name]['points'][0]
                    y = obj.state[name]['points'][1]
                    x_zomb = obj.state[zomb]['points'][0]
                    y_zomb = obj.state[zomb]['points'][1]

                    if abs(x - x_zomb) <= self.run_away_range:
                        x -= self.run_away
                    else:
                        x += self.run_away
                    if abs(y - y_zomb) <= self.run_away_range:
                        y -= self.run_away
                    else:
                        y += self.run_away

                    coord = [x, y]
                    self.init_aim_in_object(obj,name, coord=coord)

                if obj.state[name]['props']['is_find_aim'] and not is_run_away:
                    if self.aims['old_aims'][obj.state[name]['props']['aim_count']] == self.aims['new_aims'][obj.state[name]['props']['aim_count']]:
                        obj.state[name]['props']['is_find_aim'] = False

                if obj.state[name]['props']['is_find_aim'] == False and not is_run_away:
                    first = self.aims['new_aims'][0]
                    second = self.aims['new_aims'][1]
                    x = obj.state[name]['points'][0]
                    y = obj.state[name]['points'][1]

                    if obj.compare_lists_by_sum([abs(first[0] -  x), abs(first[1] - y)],[abs(second[0] - x), abs(second[1] - y)]):
                        obj.state[name]['props']['aim'] = [*first]
                        obj.state[name]['props']['aim_count'] = 0
                    else:
                        obj.state[name]['props']['aim'] = [*second]
                        obj.state[name]['props']['aim_count'] = 1

            elif obj.state[name]['props']['is_zombie']:
                min_points = self.bot_manager.zombie_stalking(obj=obj, name=name)
                self.init_aim_in_object(obj, name=name, is_zomb=True, coord=min_points)
            