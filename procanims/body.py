import math
import pygame

class Segment:
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
        return self.x+math.cos(math.radians(angle))*self.size*0.99, self.y+math.sin(math.radians(angle))*self.size*0.99
    
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
        return f"Segment({self.x}, {self.y}, {self.size})"
    def __repr__(self): return str(self)

class Animal:
    def __init__(self, segments, constrainSize=None):
        self.segments = segments
        self.conSze = constrainSize
    
    def set_pos(self, pos):
        self.segments[-1].pos = pos
        self.constrain_all()
    
    def constrain_all(self):
        for i in range(len(self.segments)-1, 0, -1):
            self.segments[i-1].constrain(self.segments[i].pos, self.conSze)
    
    def draw(self, win):
        for p in self.segments:
            pygame.draw.circle(win, (255, 255, 255), p.pos, p.size)
        
        newps = []
        tmp = []
        for i in range(len(self.segments)):
            if i == len(self.segments) - 1:
                ps2 = [90, 135, 180, -135, -90]
                ang = self.segments[i - 1].angleTo(self.segments[i])
            else:
                ang = self.segments[i].angleTo(self.segments[i + 1])
                if i == 0:
                    ps2 = [-90, -45, 0, 45, 90]
                else:
                    ps2 = [90, -90]
            for j in ps2:
                newp = self.segments[i].findOnCircle(ang + j)
                #pygame.draw.circle(win, (255, 50, 50), newp, 2, 3)
                if i == len(self.segments) - 1 or i == 0:
                    newps.append(newp)
                else:
                    if j == 90:
                        newps.append(newp)
                    else:
                        tmp.append(newp)
        newps.extend(tmp[::-1])
        pygame.draw.polygon(win, (255, 255, 255), newps)
    
    def __getitem__(self, key):
        return self.segments[key]
    
    def __iter__(self):
        return iter(self.segments)
    def __len__(self):
        return len(self.segments)

    def __str__(self):
        return f"Animal({self.segments}, {self.conSze})"
    def __repr__(self): return str(self)
