import pygame 
from pygame.locals import *
from gl import Renderer

width = 960
height = 540

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.glColor(1,0,1)
rend.glClearColor(1,0.5,1)

isRunning = True 
while isRunning:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rend.glClear()
    
    for i in range(100):    
        rend.glPoint(480 +i ,270+i)
                
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()    
