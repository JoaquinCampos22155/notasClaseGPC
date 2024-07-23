import pygame 
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import vertexShader
width = 960
height = 540

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.glColor(1,0.2,0.4)


modelo1 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/guitarra.obj")
modelo1.translate[0] = width/2
modelo1.translate[1] = height/2

modelo1.scale[0] = 120
modelo1.scale[1] = 120
modelo1.scale[2] = 120




rend.models.append(modelo1)


isRunning = True 
while isRunning:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                
            elif event.key == pygame.K_RIGHT:
                modelo1.rotate[1] += 30
            elif event.key == pygame.K_LEFT:
                modelo1.rotate[1] -= 30
            elif event.key == pygame.K_UP:
                modelo1.rotate[2] += 30
            elif event.key == pygame.K_DOWN:
                modelo1.rotate[2] -= 30
            elif event.key == pygame.K_h:
                modelo1.rotate[0] += 30
            elif event.key == pygame.K_j:
                modelo1.rotate[0] -= 30

    rend.glClear()
    rend.glRender()
        
                
    pygame.display.flip()
    clock.tick(60)
rend.glGFB("clase1/ejercicio1output/output.bmp")    
pygame.quit()    
