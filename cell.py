from static import Static

class Cell:
    # Main character class
    def __init__(self, x, y) -> None:
        self.static = Static()
        self.props = self.static.get_cell_data()['props']
        self.x = x
        self.y = y

    def init_cell(self, state_instance, is_hero=False, hero_config={}):
        state_instance._add_object_to_dictionary(
            {
                'points': (self.x, self.y),
                'old_points': (self.x, self.y),
                'is_hero': is_hero,
                'props': self.props,
            },
            is_hero, hero_config
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
            'size': 8
        }

    # not yet thought of useful in the future
    def change_propirties(self):
        pass
