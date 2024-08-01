import pygame 
from pygame.locals import *
from gl import *
from model import Model
from shaders import vertexShader
width = 960
height = 540

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.glColor(1,0.2,0.4)

#guitarra
modelo1 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/guitarra.obj")
modelo1.translate[0] = width/2
modelo1.translate[1] = height/3

modelo1.scale[0] = 100
modelo1.scale[1] = 100
modelo1.scale[2] = 100

#Cara

# modelo2 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/face.obj")
# modelo2.translate[0] = width/4*3
# modelo2.translate[1] = height/3

# modelo2.scale[0] = 10
# modelo2.scale[1] = 10
# modelo2.scale[2] = 10

rend.models.append(modelo1)
#rend.models.append(modelo2)


isRunning = True
modelo1.rotate[1] += 90

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                
            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 30
            elif event.key == pygame.K_LEFT:
                rend.camera.translate[0] -= 30
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] += 30
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] -= 30
            elif event.key == pygame.K_d:
                rend.camera.rotate[0] += 30
            elif event.key == pygame.K_a:
                rend.camera.rotate[0] -= 30
            elif event.key == pygame.K_w:
                rend.camera.rotate[1] += 30
            elif event.key == pygame.K_s:
                rend.camera.rotate[1] -= 30
            elif event.key == pygame.K_r:
                rend.camera.rotate[2] += 10
            elif event.key == pygame.K_f:
                rend.camera.rotate[2] -= 10
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            elif event.key == pygame.K_v:
                rend.glGFB("clase/ImagenesLab3/ImagenesLab3_Lineas/midiumshot.bmp")    
            elif event.key == pygame.K_b:
                rend.glGFB("clase/ImagenesLab3/ImagenesLab3_Lineas/lowangle.bmp")   
            elif event.key == pygame.K_n:
                rend.glGFB("clase/ImagenesLab3/ImagenesLab3_Lineas/highangle.bmp")   
            elif event.key == pygame.K_m:
                rend.glGFB("clase/ImagenesLab3/ImagenesLab3_Lineas/dutchangle.bmp")   


    rend.glClear()
    rend.glRender()
        
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()  
  
