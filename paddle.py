class Paddle:
    def __init__(self, x, y, width, height, vel):
        self.vel = vel
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

    def move(self, up=True):
        if(up):
            self.y -= self.vel
        else:
            self.y += self.vel