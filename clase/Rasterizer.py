import pygame 
from pygame.locals import *
from gl import *
from model import Model
from shaders import *

width = 600
height = 500 

# dimensiones con z
# width = 200
# height = 200
screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.glLoadBackground("clase/textures/backgroundspace.bmp")

# #EJERCICIO
r = 0.75
g = 0.75
b = 0.75


#mundo
modelo2 = Model("clase/objects/Earth.obj")

modelo2.vertexShader = vertexShader
modelo2.fragmentShader = majoraskShader

modelo2.LoadTexture("clase/textures/earth/Diffuse.bmp")
modelo2.translate[0] = -2
modelo2.translate[1] = -1.5 
modelo2.translate[2] = -5
modelo2.scale[0] = 0.3
modelo2.scale[1] = 0.3
modelo2.scale[2] = 0.3
#mesa
modelo3 = Model("clase/objects/table.obj")
modelo3.LoadTexture("clase/textures/madera1.bmp")
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = waffleShader
modelo3.translate[0] = 1
modelo3.translate[1] = 0.8
modelo3.translate[2] = -5
modelo3.rotate[1] = -50
modelo3.rotate[0] = -25
modelo3.scale[0] = 1
modelo3.scale[1] = 1
modelo3.scale[2] = 1

#Luna
modelo4 = Model("clase/objects/Moon.obj")
modelo4.LoadTextures("clase/textures/moon/Bump.bmp")
modelo4.LoadTextures("clase/textures/moon/Diffuse.bmp")


modelo4.vertexShader = vertexShader
modelo4.fragmentShader = majoraskShader


modelo4.translate[0] = 2
modelo4.translate[1] = 4  
modelo4.translate[2] = -3
modelo4.scale[0] = 0.3
modelo4.scale[1] = 0.3
modelo4.scale[2] = 0.3


rend.models.append(modelo2)
rend.models.append(modelo3)
# rend.models.append(modelo4)


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
    rend.glClearBackground()
    rend.glRender()
    pygame.display.flip()	  
    clock.tick(60)
rend.glGFB("edgesgreenShader.bmp")

pygame.quit()  
  
