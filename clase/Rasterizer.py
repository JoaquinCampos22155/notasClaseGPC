import pygame 
from pygame.locals import *
from gl import *
from model import Model
from shaders import *

width = 940
height = 450 
#background_color = (155, 155, 155)  # Color de fondo en RGB (gris)
background_color = (0, 0, 0)  # Color de fondo en RGB (negro)

# dimensiones con z
# width = 200
# height = 200
screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)


# #EJERCICIO
# modelo1 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/objects/face.obj")
r = 0.75
g = 0.75
b = 0.75

# modelo1.scale[0] = 2 
# modelo1.scale[1] = 2
# modelo1.scale[2] = 2

 
#Cara
# modelo1 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/objects/table.obj")
# modelo1.LoadTexture("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/textures/madera1.bmp")
# modelo1.vertexShader = vertexShader
# modelo1.fragmentShader = bywshader

# modelo1.translate[2] = -3
# modelo1.translate[0] = -2
# modelo1.translate[1] = -1  
# modelo1.scale[0] = 2
# modelo1.scale[1] = 2
# modelo1.scale[2] = 2

modelo2 = Model("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/objects/table.obj")
modelo2.LoadTexture("C:/Users/jjcam/Desktop/Semestre_6/GraficasPC/notasClaseGPC/clase/textures/madera1.bmp")
modelo2.vertexShader = vertexShader
modelo2.fragmentShader = majoraskShader

modelo2.translate[2] = -3
modelo2.translate[0] = 0
modelo2.translate[1] = -1
modelo2.scale[0] = 2
modelo2.scale[1] = 2
modelo2.scale[2] = 2

# rend.models.append(modelo1)
rend.models.append(modelo2)



isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            
            #perspectiva camara "X"
            elif event.key == pygame.K_LEFT:
                rend.camera.translate[0] += 1
            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] -= 1
            
            #perspectiva camara "Y"
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] += 1
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] -= 1
            
            #rotacion camara 
            elif event.key == pygame.K_s:
                rend.camera.rotate[0] += 30
            elif event.key == pygame.K_w:
                rend.camera.rotate[0] -= 30
            elif event.key == pygame.K_d:
                rend.camera.rotate[1] += 30
            elif event.key == pygame.K_a:
                rend.camera.rotate[1] -= 30
            elif event.key == pygame.K_r:
                rend.camera.rotate[2] += 30
            elif event.key == pygame.K_f:
                rend.camera.rotate[2] -= 30
            
            #perspectiva camara "Z"
            elif event.key == pygame.K_9:
                rend.camera.translate[2] += 5
            elif event.key == pygame.K_8:
                rend.camera.translate[2] -= 5
            
            #tipo rend
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES  
    rend.glClear()
    screen.fill(background_color)
    rend.glRender()
    pygame.display.flip()	  
    clock.tick(60)
rend.glGFB("majoraskshader.bmp")

pygame.quit()  
  
