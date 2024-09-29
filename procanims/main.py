import pygame
import math
pygame.init()
win = pygame.display.set_mode((1000, 1000))

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
        phi = math.atan2(oy - self.y, ox - self.x)-math.pi
        self.x, self.y = ox+math.cos(phi)*osize, oy+math.sin(phi)*osize
    
    def findOnCircle(self, angle):
        return self.x+math.cos(math.radians(angle))*self.size, self.y+math.sin(math.radians(angle))*self.size
    
    def angleTo(self, opoint):
        return math.degrees(math.atan2(opoint[1] - self.y, opoint[0] - self.x))-180 % 360
    
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

ps = [Point(250, 250, i) for i in [29, 35, 39, 52, 45]]

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
        ps[i].constrain(ps[i+1])#, 25)#42)
    
    for p in ps:
        pygame.draw.circle(win, (255, 255, 255), p.pos, p.size, 4)
    
    newps = []
    tmp = []
    for i in range(len(ps)):
        if i == len(ps) - 1:
            ps2 = [90, 135, 180, -135, -90]
            ang = ps[i - 1].angleTo(ps[i])
        else:
            ang = ps[i].angleTo(ps[i + 1])
            if i == 0:
                ps2 = [-90, -45, 0, 45, 90]
            else:
                ps2 = [90, -90]
        for j in ps2:
            newp = ps[i].findOnCircle(ang + j)
            pygame.draw.circle(win, (255, 50, 50), newp, 2, 3)
            if i == len(ps) - 1 or i == 0:
                newps.append(newp)
            else:
                if j == 90:
                    newps.append(newp)
                else:
                    tmp.append(newp)
    newps.extend(tmp[::-1])
    
    pygame.draw.polygon(win, (10, 255, 50), newps, 10)

    pygame.display.update()
    clock.tick(60)
