import pygame 
from pygame.locals import *
from gl import *
from model import Model
from shaders import vertexShader

# width = 960
# height = 540

width = 200
height = 200
screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.glColor(1,0.2,0.4)



# #guitarra
# modelo1 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/guitarra.obj")

# modelo1.translate[2] = -500
# modelo1.rotate[0] = 90
# modelo1.rotate[2] = -90


# modelo1.scale[0] = 100
# modelo1.scale[1] = 100
# modelo1.scale[2] = 100

# #Cara

# modelo2 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/face.obj")
# modelo2.translate[2] = 500

# modelo2.scale[0] = 10
# modelo2.scale[1] = 10
# modelo2.scale[2] = 10

rend.models.append(modelo1)
#rend.models.append(modelo2)


isRunning = True
modelo1.rotate[1] += 90
#rend.models.append(modelo1)
# rend.models.append(modelo2)

triangle1 = [[10,70],[50,160],[70,80]]
triangle2 = [[180,50],[150,1],[70,180]]
triangle3 = [[180,150],[120,160],[130,180]]


isRunning = True
#modelo1.rotate[1] += 90

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
                
            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 50
            elif event.key == pygame.K_LEFT:
                rend.camera.translate[0] -= 50
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] += 50
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] -= 50
            elif event.key == pygame.K_d:
                rend.camera.rotate[0] += 30
            elif event.key == pygame.K_a:
                rend.camera.rotate[0] -= 30
            elif event.key == pygame.K_w:
                rend.camera.rotate[1] += 30
            elif event.key == pygame.K_s:
                rend.camera.rotate[1] -= 30
            elif event.key == pygame.K_r:
                rend.camera.rotate[2] += 30
            elif event.key == pygame.K_f:
                rend.camera.rotate[2] -= 30
            elif event.key == pygame.K_9:
                rend.camera.translate[2] += 50
            elif event.key == pygame.K_8:
                rend.camera.translate[2] += 50
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
    #rend.glRender()
    rend.glTriangle(triangle1[0], triangle1[1], triangle1[2])
    rend.glTriangle(triangle2[0], triangle2[1], triangle2[2])
    rend.glTriangle(triangle3[0], triangle3[1], triangle3[2])

        
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()  
  
