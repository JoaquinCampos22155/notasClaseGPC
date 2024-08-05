import struct 
import model as model
from camera import Camera
from pygame import *
from math import tan, pi
from Mathlib import barycentricCoords
import random
def char(c):
    #1 byte
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    #2 bytes
    return struct.pack("=h", w)

def dword(d):
    #4 bytes
    return struct.pack("=l", d)

POINTS = 0
LINES = 1
TRIANGLE = 2
QUADS = 3

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        
        self.camera = Camera()
        self.glViewport(0, 0 , self.width, self.height)
        self.glProjection()
        
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()
    
        self.vertexShader = None
        
        self.primitiveType = POINTS
        
        self.models = []
    
    def glViewport(self, x, y , width, height ):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpwidth= width
        self.vpheight = height
        
        self.viewportMatrix = [[width/2,0,0,x+ width/2],
                            [0,height/2,0,y + height/2],
                            [0,0,0.5,0.5],
                            [0,0,0,1]]
        
    def glProjection(self, n =0.1, f = 1000, fov = 60 ):
        aspectRatio = self.vpwidth/self.vpheight
        #rads por tan de math
        fov *= pi/180
        t = tan(fov/2) * n
        r = t * aspectRatio 

        self.projectionMatrix = [[n/r,0,0,0],
                            [0,n/t,0,0],
                            [0,0,-(f+n)/(f-n),-(2*f*n)/(f-n)],
                            [0,0,-1,0]]
        
    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))
        self.currColor = [r,g,b]
        
    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))    
        self.clearColor = [r,g,b]
        
    def glClear(self):
        color = [int(i*255) for i in self.clearColor]
        self.screen.fill(color)
        
        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]
        
    def glPoint(self, x, y, color = None):
        #pygame renderiza desde esquina superior iquerida    
        if (0<=x<self.width) and (0<=y<self.height):
            color = [int(i*255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)    
            self.frameBuffer[x][y] = color
            
    def glLine(self, v0, v1, color = None):
        #formula es y = mx+b
        
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])
        
        #Algoritmo de lineas de Bresenham
        
        #si punto 0 es igual al punto 1 en x y y o sea solo un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        steep = dy > dx
        
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0) 
        
        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0
        
        for x in range(x0, x1+1):
            if steep:
                self.glPoint(y,x, color or self.currColor)
            else:       
                self.glPoint(x, y, color or self.currColor)
            
            offset += m 
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else: 
                    y -= 1
                limit += 1
                
    def glGFB(self, filename):       
        with open(filename, "wb") as file: 
            #header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 +40))
            
            #info header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height *3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            
            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2], color[1], color[0]])
                    file.write(color)
                    
                    
    def glRender(self):
        for model in self.models:
            #por cada modelo en la lista lo voy a dibujar
            #agarra su matriz modelo
            mMat = model.GetModelMatrix()
            
            vertexBuffer = [ ]
            
            #para cada cara del modelo
            
            for face in model.faces:
                #revisar vertices por cara
                vertCount = len(face)
                v0 = model.vertices[face[0][0] -1]
                v1 = model.vertices[face[1][0] -1]
                v2 = model.vertices[face[2][0] -1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]
                #si hay vertex shader
                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix = mMat ,viewMatrix = self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    v1 = self.vertexShader(v1, modelMatrix = mMat ,viewMatrix = self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    v2 = self.vertexShader(v2, modelMatrix = mMat ,viewMatrix = self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    if vertCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix = mMat, viewMatrix = self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                
                vertexBuffer.append(v0)
                vertexBuffer.append(v1)
                vertexBuffer.append(v2)
                if vertCount == 4:
                    vertexBuffer.append(v0)
                    vertexBuffer.append(v2)
                    vertexBuffer.append(v3)
                    
            self.glDrawPrimitives(vertexBuffer)
         
            self.glPoint(int(v0[0]), int(v0[1]))
            self.glPoint(int(v1[0]), int(v1[1]))
            self.glPoint(int(v2[0]), int(v2[1]))
            if vertCount == 4:
                self.glPoint(int(v3[0]), int(v3[1]))

                    
            
    def glTriangle(self, A, B, C):
        if  A[1]<B[1]:
            A, B = B, A
        if A[1] <C[1]:
            A,C = C, A
        if B[1] <C[1]:
            B,C = C,B
        
        def flatBottom(vA, vB, vC):
            try:
                mBA = (vB[0] -vA[0])/(vB[1] -vA[1])
                mCA = (vC[0] -vA[0])/(vC[1] -vA[1])
            except: 
                pass
            else:
                x0 = vB[0]
                x1 = vC[0]
                for y in range (round(vB[1]), round(vA[1]+1)):
                    #self.glLine([x0,y], [x1,y], color)
                    for x in range(round(x0), round(x1+1) ):
                        vP = [x,y]
                        bCoords = barycentricCoords(vA,vB, vC, vP)
                        if bCoords != None:
                            u,v,w = bCoords
                            r = u*vA[3] +v*vB[3] +w*vC[3]
                            g = u*vA[4] +v*vB[4] +w*vC[4]
                            b = u*vA[5] +v*vB[5] +w*vC[5]
                            color = [r,g,b]
                        self.glPoint(x,y, color)
                    x0 += mBA
                    x1 += mCA
                    
        def flatTop(vA, vB, vC):
            try:
                mCA = (vC[0] -vA[0])/(vC[1] -vA[1])
                mCB = (vC[0] -vB[0])/(vC[1] -vB[1])
            except: 
                pass
            else:
                x0 = vA[0]
                x1 = vB[0]
                for y in range (round(vA[1]), round(vC[1]-1), -1):
                    #self.glLine([x0,y], [x1,y], color)
                    for x in range(round(x0), round(x1+1) ):
                        vP = [x,y]
                        bCoords = barycentricCoords(vA,vB, vC, vP)
                        if bCoords != None:
                            u,v,w = bCoords
                            r = u*vA[3] +v*vB[3] +w*vC[3]
                            g = u*vA[4] +v*vB[4] +w*vC[4]
                            b = u*vA[5] +v*vB[5] +w*vC[5]
                            color = [r,g,b]
                        self.glPoint(x,y, color)
                    x0 -= mCA
                    x1 -= mCB                  
                
            
        if B[1] == C[1]:
            #parte plana abajo 
            flatBottom(A, B, C)
        elif A[1] == B[1]:
            #parte plana arriba
            flatTop(A, B, C)
        else:
            #divido el triangulo en dos partes 
            #y dibujo ambos tipos de triangulos
            #teorema intercepto
            D = [A[0] + ((B[1] -A[1]) / (C[1] - A[1])) * (C[0] -A [0]), B[1]]
            flatBottom(A, B, D)
            flatTop(B, D, C)
        
    def glDrawPrimitives(self, buffer):
        if self.primitiveType == POINTS:
                for point in buffer:
                    self.glPoint(int(point[0]), int(point[1]))
        elif self.primitiveType == LINES:
            for i in range(0, len(buffer), 3):
                p0 = buffer[i]
                p1 = buffer[i+1]
                p2 = buffer[i+2]
                
                self.glLine((p0[0], p0[1]),(p1[0], p1[1]))
                self.glLine((p1[0], p1[1]),(p2[0], p2[1]))
                self.glLine((p2[0], p2[1]),(p0[0], p0[1]))
        elif self.primitiveType == TRIANGLE:
            for i in range(0, len(buffer), 3):
                p0 = buffer[i]
                p1 = buffer[i+1]
                p2 = buffer[i+2] 
                #color = [random.random(), random.random(), random.random()]
                self.glTriangle(p0,p1,p2) 
                    