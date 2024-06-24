class Static:

    def get_hero_data(self):
        return {
            'hero_config': {'speed': 15, 'color': [0.3,0.7,1], 'size': 11},
            'spawn_point': [50, 50], 
            }
    
    def get_spawn_aim_range(self):
        return {"min": 10, 'max': 90}
    
    def get_zombie_data(self):
        return {
            "color": [0, 1, 0],
            "speed": [1, 1],

        }
    
    def get_cell_data(self):
        return {
            "vision_range": [2,2],
            'run_away': 0.1,
            'run_away_range': 5,
            "props": {
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
        }

    def get_borders_data(self):
        return {
            "min_border": 0,
            "max_border": 100,
        }
    
    def get_collision_data(self):
        return {
            'reaction_force': 0.1,
            'accuracy': 0.03,
        }
    
    def get_window_data(self):
        return {
            'resolution': [600, 600]
        }
    def get_game_data(self):
        return {
            'fps': 60,
            'count_of_objects': 20,
        }