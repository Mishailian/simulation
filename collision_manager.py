from math import isclose
from static import Static


class Collision_manager:

    def __init__(self) -> None:
         self.static = Static()
         self.reaction_force = self.static.get_collision_data()['reaction_force']
         self.accuracy = self.static.get_collision_data()['accuracy']

    def case_variation_handling(self, is_x_close, is_y_close, reaction_force, ob_gravity, name_gravity, name, ob, obj):
            ''' 
             taking into account different situations
             1 if one negative another negative too
             2 if one positive another positive too
             3 if one positive another negtive
             4 if one negative another positive
            '''

            if is_x_close and is_y_close and ob_gravity and name_gravity:
                obj.state[name]['points'] = (
                    obj.state[name]['old_points'][0] - reaction_force, obj.state[name]['old_points'][1] - reaction_force)
                obj.state[ob]['points'] = (
                    obj.state[ob]['old_points'][0] - reaction_force, obj.state[ob]['old_points'][1] - reaction_force)

            if is_x_close and is_y_close and ob_gravity == False and name_gravity == False:
                obj.state[name]['points'] = (
                    obj.state[name]['old_points'][0] + reaction_force, obj.state[name]['old_points'][1] + reaction_force)
                obj.state[ob]['points'] = (
                    obj.state[ob]['old_points'][0] + reaction_force, obj.state[ob]['old_points'][1] + reaction_force)

            if is_x_close and is_y_close and ob_gravity == False and name_gravity:
                obj.state[name]['points'] = (
                    obj.state[name]['old_points'][0] + reaction_force, obj.state[name]['old_points'][1] + reaction_force)
                obj.state[ob]['points'] = (
                    obj.state[ob]['old_points'][0] - reaction_force, obj.state[ob]['old_points'][1] - reaction_force)

            if is_x_close and is_y_close and ob_gravity and name_gravity == False:
                obj.state[name]['points'] = (
                    obj.state[name]['old_points'][0] - reaction_force, obj.state[name]['old_points'][1] - reaction_force)
                obj.state[ob]['points'] = (
                    obj.state[ob]['old_points'][0] + reaction_force, obj.state[ob]['old_points'][1] + reaction_force)

    def collision(self, obj, name):
        state = obj.show_state()
        name_gravity = obj.state[name]['props']['is_negative_gravity']

        for ob in state: # !!!!!!!!!!!!!!!!! 
            ob_gravity = obj.state[ob]['props']['is_negative_gravity']
            is_x_close = isclose(
                state[name]['points'][0], state[ob]['points'][0], rel_tol=self.accuracy)
            is_y_close = isclose(
                state[name]['points'][1], state[ob]['points'][1], rel_tol=self.accuracy)
            self.case_variation_handling(is_x_close, is_y_close, obj=obj, ob=ob, name=name,ob_gravity=ob_gravity, reaction_force=self.reaction_force, name_gravity=name_gravity)