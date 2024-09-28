import pygame
import math
pygame.init()
win = pygame.display.set_mode((500, 500))

class Point:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    
    @property
    def pos(self):
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, value):
        self.x, self.y = value
    
    def constrain(self, opoint, osize=None):
        ox, oy = opoint[0], opoint[1]
        if osize is None:
            osize = opoint[2]
        phi = math.degrees(math.atan2(oy - self.y, ox - self.x))-180 % 360
        self.x, self.y = ox+math.cos(math.radians(phi))*osize, oy+math.sin(math.radians(phi))*osize
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.size
        else:
            raise IndexError("Index out of range")
    
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.size = value
        else:
            raise IndexError("Index out of range")
    
    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.size})"
    def __repr__(self): return str(self)

ps = [Point(250, 250, 25), Point(250, 250, 25), Point(250, 250, 25), Point(250, 250, 25)]

clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    win.fill((0, 0, 0))

    ps[-1].pos = pygame.mouse.get_pos()
    for i in range(len(ps)-1):
        ps[i].constrain(ps[i+1])
    
    for p in ps:
        pygame.draw.circle(win, (255, 255, 255), p.pos, p.size, 4)

    pygame.display.update()
    clock.tick(60)
