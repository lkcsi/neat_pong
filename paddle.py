class Paddle:
    VEL = 4
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

    def move(self, up=True):
        if(up):
            self.y -= self.VEL
        else:
            self.y += self.VEL