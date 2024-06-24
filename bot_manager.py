from math import isclose
from static import Static

class Bot_manager: 

    def __init__(self) -> None:
        self.static = Static()
        self.zombie_color = self.static.get_zombie_data()['color']
        self.zombie_speed = self.static.get_zombie_data()['speed']

    def zombie_stalking(self, obj, name):
        x = obj.state[name]['points'][0]
        y = obj.state[name]['points'][1]
        min_points = [obj.state[name]['props']['aim'][0], obj.state[name]['props']['aim'][1]]
        for ob in obj.state:
            # for that if object dont pic him obj
            if name != ob and not obj.state[ob]['props']['is_zombie']:
                if obj.compare_lists_by_sum([abs(min_points[0] - obj.state[ob]['points'][0]),abs(min_points[1] - obj.state[ob]['points'][1])], [40,40]):
                    min_points[0] = obj.state[ob]['points'][0]
                    min_points[1] = obj.state[ob]['points'][1]
                elif isclose(x, obj.state[ob]['points'][0], abs_tol=1) and isclose(y, obj.state[ob]['points'][1], abs_tol=1):
                    obj.state[ob]['props']['is_zombie'] = True
                    obj.state[ob]['props']['color'] = self.zombie_color
                    obj.state[ob]['props']['speed'] = self.zombie_speed

        return min_points