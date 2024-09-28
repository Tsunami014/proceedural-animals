import pygame
import math
pygame.init()
win = pygame.display.set_mode((500, 500))

def constrain(point, opoint):
    x, y = point[0] - opoint[0], point[1] - opoint[1]
    phi = math.degrees(math.atan2(y, x))-180 % 360
    return (point[0]+math.cos(math.radians(phi))*25, point[1]+math.sin(math.radians(phi))*25)

ps = [[250, 250], [250, 250], [250, 250], [250, 250]]

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

    ps[-1] = pygame.mouse.get_pos()
    for p in range(len(ps)-1):
        ps[p] = constrain(ps[p+1], ps[p])
        pygame.draw.circle(win, (255, 255, 255), ps[p], 10)
    pygame.draw.circle(win, (255, 255, 255), pygame.mouse.get_pos(), 10)

    pygame.display.update()
    clock.tick(60)
