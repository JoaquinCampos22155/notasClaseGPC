import pygame 
from pygame.locals import *
from gl import Renderer

width = 960
height = 540

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

rend = Renderer(screen)



isRunning = True 
while isRunning:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rend.glClear()
    
    punto0 = (width / 2, height /2)
    
    for x in range (0, width,10 ):
        rend.glLine(punto0, (x, height))
        rend.glLine(punto0, (x, -height))
        
    
    for x in range (0, width, 20):
        rend.glLine((0,0), (x, height))
        rend.glLine((0, height -1) ,(x, 0))
        rend.glLine((width -1,0), (x, height)) 
        rend.glLine((width -1, height -1) ,(x, 0))
                
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()    
