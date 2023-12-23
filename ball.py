class Ball:
    MAX_VEL = 6
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = 0
        self.y_vel = 0

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = 0
        self.y_vel = 0

    def left(self):
        return self.x - self.radius 

    def right(self):
        return self.x + self.radius 

    def top(self):
        return self.y - self.radius
    
    def bottom(self):
        return self.y + self.radius