import pygame
from enum import Enum

class layer(Enum):
    BEHIND = 0
    FRONT = 1

class Eyes:
    lay = layer.FRONT
    def draw(self, win, body, seg, angle):
        pygame.draw.circle(win, (0, 0, 0), seg.findOnCircle(angle-45, 0.7), 5)
        pygame.draw.circle(win, (0, 0, 0), seg.findOnCircle(angle+45, 0.7), 5)

class Fin:
    lay = layer.BEHIND
    def __init__(self, col, size=(30, 50), angle=30, buffersze=2):
        self.col = col
        self.size = size
        self.angle = angle
        self.buffer = []
        self.buffersze = buffersze
    
    def draw(self, win, body, seg, origangle):
        fin = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.ellipse(fin, self.col, (0, 0, *self.size))

        self.buffer.append(origangle)
        angle = self.buffer[0]
        if len(self.buffer) > self.buffersze:
            del self.buffer[0]
        
        def offset(pos, f):
            return (pos[0]-f.get_width()//2, pos[1]-f.get_height()//2)
        fin1 = pygame.transform.rotate(fin, -angle-90-self.angle)
        fin2 = pygame.transform.rotate(fin, -angle-90+self.angle)
        win.blit(fin1, offset(seg.findOnCircle(angle-90, 0.8), fin1))
        win.blit(fin2, offset(seg.findOnCircle(angle+90, 0.8), fin2))
