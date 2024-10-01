try:
    from procanims.body import makeAnimal
except ImportError:
    from body import makeAnimal
import pygame
pygame.init()
win = pygame.display.set_mode((1000, 1000))

anim = makeAnimal(list(range(10, 20)) + [27, 25], 42, bodyColour=(255, 50, 50))

clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    win.fill(pygame.color.THECOLORS["skyblue"])

    anim.set_pos(pygame.mouse.get_pos())

    anim.draw(win)

    pygame.display.update()
    clock.tick(60)
