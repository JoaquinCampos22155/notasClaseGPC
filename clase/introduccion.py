import pygame 
from pygame.locals import *
from gl import Renderer

width = 960
height = 540

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.glColor(1,0.2,0.4)


poligono1 = ((165, 380) ,(185, 360) ,(180, 330), (207, 345),  (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383))
poligono2 = ((321, 335), (288, 286), (339, 251), (374, 302))
poligono3 = ((377, 249), (411, 197), (436, 249))
poligono4 = ((413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
            (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
            (597, 215), (552, 214), (517, 144), (466, 180))
poligono5 = ((682, 175), (708, 120), (735, 148), (739, 170))

def drawPoligono(listapuntos, fill=False):
    # Dibuja los bordes del polígono
    for i in range(len(listapuntos)):
        rend.glLine(listapuntos[i], listapuntos[(i+1) % len(listapuntos)])

    if fill:
        # Encuentra el bounding box del polígono
        min_x = min(point[0] for point in listapuntos)
        max_x = max(point[0] for point in listapuntos)
        min_y = min(point[1] for point in listapuntos)
        max_y = max(point[1] for point in listapuntos)

        # Scanline fill algorithm
        for x in range(min_x, max_x + 1):
            intersections = []
            for i in range(len(listapuntos)):
                p1 = listapuntos[i]
                p2 = listapuntos[(i+1) % len(listapuntos)]
                if p1[0] == p2[0]:  # Ignorar líneas verticales
                    continue
                if x < min(p1[0], p2[0]) or x > max(p1[0], p2[0]):  # Ignorar fuera del rango de la línea
                    continue
                # Encontrar el punto de intersección con la línea vertical en x
                y = p1[1] + (x - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0])
                intersections.append((y, p1, p2))

            intersections.sort()

            # Procesar intersecciones para evitar duplicados en vértices
            unique_intersections = []
            skip_next = False
            for j in range(len(intersections) - 1):
                if skip_next:
                    skip_next = False
                    continue
                y1, p1_1, p2_1 = intersections[j]
                y2, p1_2, p2_2 = intersections[j + 1]
                if y1 == y2:
                    if (p1_1[1] > y1 and p2_1[1] > y1) or (p1_1[1] < y1 and p2_1[1] < y1):
                        unique_intersections.append(y1)
                    skip_next = True
                else:
                    unique_intersections.append(y1)
            if not skip_next and intersections:
                unique_intersections.append(intersections[-1][0])

            # Asegurarse de que el número de intersecciones sea par
            if len(unique_intersections) % 2 == 1:
                unique_intersections.pop()

            for j in range(0, len(unique_intersections), 2):
                for y in range(int(unique_intersections[j]), int(unique_intersections[j+1]) + 1):
                    rend.glPoint(x, y)

isRunning = True 
while isRunning:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rend.glClear()
        
    drawPoligono(poligono1, fill=True)
    drawPoligono(poligono2, fill=True)
    drawPoligono(poligono3, fill=True)
    drawPoligono(poligono4, fill=True)
    drawPoligono(poligono5, fill=False)
                
    pygame.display.flip()
    clock.tick(60)
rend.glGFB("clase1/ejercicio1output/output.bmp")    
pygame.quit()    
