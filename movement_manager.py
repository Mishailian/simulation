from math import isclose

class Movement_manager:
    def __init__(self) -> None:
        pass
    
    def main(self, obj, aim, points):
        speed_x = obj['props']['speed'][0]
        speed_y = obj['props']['speed'][1]
        x = points[0]
        y = points[1]
        if x < aim[0]:
            x += speed_x
        if x > aim[0]:
            x -= speed_x
        if y < aim[1] and (False == (isclose(y, aim[1], rel_tol=0.001))):
            y += speed_y
        if y > aim[1] and (False == (isclose(y, aim[1], rel_tol=0.001))):
            y -= speed_y
        obj['points'] = (x, y)
        return (x, y)