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

    def isColliding(self, opoint):
        return math.hypot(self.x - opoint[0], self.y - opoint[1]) <= self.size + opoint[2]
    
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
    def __init__(self, segments, constrainSize=None, outlineColour=(0, 0, 0), bodyColour=(255, 255, 255)):
        self.segments = segments
        self.conSze = constrainSize

        self.outlineCol = outlineColour
        self.bodyCol = bodyColour

        # Thanks to https://www.youtube.com/watch?v=xPKuhqt8Pcs for the outline code!
        self.convolution_mask = pygame.mask.Mask((3, 3), fill = True)
        self.convolution_mask.set_at((0, 0), value = 0)
        self.convolution_mask.set_at((2, 0), value = 0)
        self.convolution_mask.set_at((0, 2), value = 0)
        self.convolution_mask.set_at((2, 2), value = 0)
    
    def set_pos(self, pos):
        self.segments[-1].pos = pos
        self.constrain_all()
    
    def constrain_all(self):
        for i in range(len(self.segments)-1, 0, -1):
            self.segments[i-1].constrain(self.segments[i].pos, self.conSze)
    
    def draw(self, win):
        newsur = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        for p in self.segments:
            pygame.draw.circle(newsur, self.bodyCol, p.pos, p.size)
        
        for i in range(len(self.segments)):
            for off in (-1, 1):
                if i+off < 0 or i+off >= len(self.segments):
                    continue
                ang = self.segments[i+off].angleTo(self.segments[i])
                newsegs = []
                for seg, js in ((self.segments[i+off], (-90, 90)), (self.segments[i], (90, -90))):
                    for j in js:
                        newp = seg.findOnCircle(ang + j)
                        #pygame.draw.circle(newsur, (255, 50, 50), newp, 2, 3)
                        newsegs.append(newp)
                pygame.draw.polygon(newsur, self.bodyCol, newsegs)
                # pygame.draw.polygon(newsur, (255, 50, 50), newsegs, 3)

        mask = pygame.mask.from_surface(newsur)
        surface_outline = mask.convolve(self.convolution_mask).to_surface(setcolor=self.outlineCol, unsetcolor=newsur.get_colorkey())
        
        surface_outline.blit(newsur, (1, 1))
        
        win.blit(surface_outline, (0, 0))
    
    def __getitem__(self, key):
        return self.segments[key]
    
    def __iter__(self):
        return iter(self.segments)
    def __len__(self):
        return len(self.segments)

    def __str__(self):
        return f"Animal({self.segments}, {self.conSze})"
    def __repr__(self): return str(self)
