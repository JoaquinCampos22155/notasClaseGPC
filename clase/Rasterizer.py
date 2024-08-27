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
#astr
modelo1 = Model("clase/objects/ast/ast1.obj")

modelo1.vertexShader = vertexShader
modelo1.fragmentShader = astShader
modelo1.LoadTextures("clase/textures/astro.bmp")
modelo1.translate[0] = 1.8
modelo1.translate[1] = -1.2 
modelo1.translate[2] = -15
modelo1.rotate[2] = 50
modelo1.rotate[1] = 50
modelo1.rotate[0] = 200
modelo1.scale[0] = 0.5
modelo1.scale[1] = 0.5
modelo1.scale[2] = 0.5

#mundo
modelo2 = Model("clase/objects/Earth.obj")

modelo2.vertexShader = vertexShader
modelo2.fragmentShader = majoraskShader
modelo2.LoadTextures("clase/textures/earth/Bump.bmp")
modelo2.LoadTextures("clase/textures/earth/Diffuse.bmp")
modelo2.translate[0] = 8
modelo2.translate[1] = 5 
modelo2.translate[2] = -15
modelo2.rotate[0] = 10
modelo2.scale[0] = 0.5
modelo2.scale[1] = 0.5
modelo2.scale[2] = 0.5
#mesa
modelo3 = Model("clase/objects/table.obj")
modelo3.LoadTexture("clase/textures/madera1.bmp")
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = waffleShader
modelo3.translate[0] = 0.8
modelo3.translate[1] = 0.6
modelo3.translate[2] = -5
modelo3.rotate[1] = -50
modelo3.rotate[0] = -25
modelo3.scale[0] = 0.8
modelo3.scale[1] = 0.8
modelo3.scale[2] = 0.8

#Luna
modelo4 = Model("clase/objects/Moon.obj")
modelo4.LoadTextures("clase/textures/moon/Bump.bmp")
modelo4.LoadTextures("clase/textures/moon/Diffuse.bmp")
modelo4.vertexShader = vertexShader
modelo4.fragmentShader = gouradShader
modelo4.translate[0] = -2
modelo4.translate[1] = -2
modelo4.translate[2] = -6
modelo4.scale[0] = 1
modelo4.scale[1] = 1
modelo4.scale[2] = 1

#Buffalo
modelo5 = Model("clase/objects/buffalo.obj")
modelo5.LoadTexture("clase/textures/buffalo/Diffuse.bmp")
modelo5.vertexShader = vertexShader
modelo5.fragmentShader = buffaloShader
modelo5.translate[0] = 9
modelo5.translate[1] = 4.5
modelo5.translate[2] = -25
modelo5.scale[0] = 1
modelo5.scale[1] = 1
modelo5.scale[2] = 1
modelo5.rotate[0] = 20
modelo5.rotate[1] = 300
modelo5.rotate[2] = 126

#alien?
modelo6 = Model("clase/objects/alien.obj")
modelo6.LoadTexture("clase/textures/alien/texture.bmp")
modelo6.vertexShader = vertexShader
modelo6.fragmentShader = alienShader
modelo6.translate[0] = -1
modelo6.translate[1] = -0.2
modelo6.translate[2] = -3
modelo6.scale[0] = 1
modelo6.scale[1] = 1
modelo6.scale[2] = 1

rend.models.append(modelo1)
rend.models.append(modelo2)
rend.models.append(modelo3)
rend.models.append(modelo4)
rend.models.append(modelo5)
rend.models.append(modelo6)

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
rend.glGFB("Proyecto1.bmp")

pygame.quit()  
  
