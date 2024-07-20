import pygame 
from pygame.locals import *
from gl import Renderer

width = 960
height = 540

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.glColor(1,0.2,0.4)


poligono1= ((165, 380) ,(185, 360) ,(180, 330), (207, 345),  (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383))


def drawPoligono(listapuntos):
     for i in range(len(listapuntos)):
        rend.glLine(listapuntos[i], listapuntos[(i+1) % len(listapuntos)])
        
        
        
isRunning = True 
while isRunning:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rend.glClear()
    
    drawPoligono(poligono1)
                
    pygame.display.flip()
    clock.tick(60)
rend.glGFB("clase1/ejercicio1output/output.bmp")    
pygame.quit()    
