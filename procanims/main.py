from procanims.body import makeAnimal
from procanims.mods import Eyes, Fin, BackFin
import pygame
pygame.init()
win = pygame.display.set_mode((1000, 1000))

def chooseAnimal(c):
    if c == 0:
        return makeAnimal(list(range(10, 20)) + [(25, Eyes())], 42, bodyColour=(255, 50, 50))
    if c == 1:
        return makeAnimal([10, (14, Fin((60, 100, 250), (20, 40))), (23, BackFin((60, 100, 250))), (30, Fin((60, 100, 250))), (25, Eyes())], 42, bodyColour=(10, 50, 255))

anim = chooseAnimal(0)

numbers = [
    pygame.K_0,
    pygame.K_1,
]

clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key in numbers:
                anim = chooseAnimal(numbers.index(event.key))
    
    win.fill(pygame.color.THECOLORS["skyblue"])

    anim.set_pos(pygame.mouse.get_pos())
    anim.draw(win)
    win.blit(pygame.font.Font(None,36).render(f'{anim.totalCurvaturePerc}%', 1, 0), (0, 0))

    pygame.display.update()
    clock.tick(60)
