import pygame

class Eyes:
    def draw(self, win, body, angle):
        pygame.draw.circle(win, (0, 0, 0), body.findOnCircle(angle-45, 0.7), 5)
        pygame.draw.circle(win, (0, 0, 0), body.findOnCircle(angle+45, 0.7), 5)
