from static import Static

class Border_manager:
    def __init__(self) -> None:
        self.static = Static()
        self.min_value = self.static.get_borders_data()['min_border']
        self.max_value = self.static.get_borders_data()['max_border']
    
    def main(self, points):
        x = points[0]
        y = points[1]
        if x < self.min_value:
            x = self.max_value - 1 
        if y < self.min_value:
            y = self.max_value - 1
        if x > self.max_value:
            x = self.min_value + 1
        if y > self.max_value:
            y = self.min_value + 1
        return (x, y)