import struct 
from camera import Camera
from math import tan, pi, isclose
from Mathlib import barycentricCoords

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
TRIANGLES = 2
QUADS = 3

class Renderer(object):
    
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        
        self.camera = Camera()
        self.glViewport(0, 0 , self.width, self.height)
        self.glProjection()
        
        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()
    
        self.vertexShader = None
        self.fragmentShader = None

        self.primitiveType = TRIANGLES
        
        self.models = []
    
    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpwidth = width
        self.vpheight = height
        
        self.viewportMatrix = [
            [width/2, 0, 0, x + width/2],
            [0, height/2, 0, y + height/2],
            [0, 0, 0.5, 0.5],
            [0, 0, 0, 1]
        ]
        
    def glProjection(self, n=0.1, f=1000, fov=60):
        aspectRatio = self.vpwidth / self.vpheight
        fov *= pi / 180
        t = tan(fov / 2) * n
        r = t * aspectRatio 

        self.projectionMatrix = [
            [n/r, 0, 0, 0],
            [0, n/t, 0, 0],
            [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
            [0, 0, -1, 0]
        ]
        
    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))
        self.currColor = [r, g, b]
        
    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))    
        self.clearColor = [r, g, b]
        
    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)
        
        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]
        self.zbuffer = [[float('inf') for y in range(self.height)]
                        for x in range(self.width)]
        
    def glPoint(self, x, y, color=None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)    
            self.frameBuffer[x][y] = color
            
    def glLine(self, v0, v1, color=None):
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])
        
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
                self.glPoint(y, x, color or self.currColor)
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
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))
            
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2], color[1], color[0]])
                    file.write(color)
                    
    def glRender(self):
        for model in self.models:
            mMat = model.GetModelMatrix()
            vertexBuffer = []
            
            for face in model.faces:
                faceVerts = []
                for i in range(len(face)):
                    vert = []
                    pos = model.vertices[face[i][0] - 1]
                    
                    if self.vertexShader:
                        pos = self.vertexShader(pos,
                                                modelMatrix=mMat,
                                                viewMatrix=self.camera.GetViewMatrix(),
                                                projectionMatrix=self.projectionMatrix,
                                                viewportMatrix=self.viewportMatrix)
                    
                    for value in pos:
                        vert.append(value)
                    faceVerts.append(vert)
                
                for value in faceVerts[0]: vertexBuffer.append(value)
                for value in faceVerts[1]: vertexBuffer.append(value)
                for value in faceVerts[2]: vertexBuffer.append(value)
                if len(faceVerts) == 4:
                    for value in faceVerts[0]: vertexBuffer.append(value)
                    for value in faceVerts[2]: vertexBuffer.append(value)
                    for value in faceVerts[3]: vertexBuffer.append(value)

            self.glDrawPrimitives(vertexBuffer, 3)

    def glTriangle(self, A, B, C):
        if A[1] < B[1]:
            A, B = B, A
        if A[1] < C[1]:
            A, C = C, A
        if B[1] < C[1]:
            B, C = C, B
            
        def flatBottom(vA, vB, vC): 
            try:
                mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
            except:
                pass
            else:
                if vB[0] > vC[0]:
                    vB, vC = vC, vB

                x0 = vB[0]
                x1 = vC[0]
                
                for y in range(round(vB[1]), round(vA[1] + 1)):
                    for x in range(round(x0 - 1), round(x1 + 1)):
                        vP = [x, y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)
                        
                    x0 += mBA
                    x1 += mCA
                    
        def flatTop(vA, vB, vC):
            try:
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
                mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])
            except:
                pass
            else:
                if vA[0] > vB[0]:
                    vA, vB = vB, vA
                    
                x0 = vA[0]
                x1 = vB[0]
                
                for y in range(round(vA[1]), round(vC[1] - 1), -1):
                    for x in range(round(x0 - 1), round(x1 + 1)):
                        vP = [x, y]
                        self.glDrawTrianglePoint(vA, vB, vC, vP)
                        
                    x0 -= mCA
                    x1 -= mCB
                    
        if B[1] == C[1]:
            flatBottom(A, B, C)
        elif A[1] == B[1]:
            flatTop(A, B, C)
        else:
            D = (C[0] + ((B[1] - C[1]) / (A[1] - C[1])) * (A[0] - C[0]), B[1])
            flatBottom(A, B, D)
            flatTop(D, B, C)
            
    def glDrawTrianglePoint(self, vA, vB, vC, vP):
        bcScreen = barycentricCoords(vA, vB, vC, vP)
        
        if (bcScreen[0] < 0 or bcScreen[0] > 1 or
            bcScreen[1] < 0 or bcScreen[1] > 1 or
            bcScreen[2] < 0 or bcScreen[2] > 1):
            return
        
        z = vA[2] * bcScreen[0] + vB[2] * bcScreen[1] + vC[2] * bcScreen[2]

        if z < self.zbuffer[vP[0]][vP[1]]:
            self.zbuffer[vP[0]][vP[1]] = z
            
            color = [bcScreen[0], bcScreen[1], bcScreen[2]]
            if self.fragmentShader:
                color = self.fragmentShader(barycentricCoords=bcScreen,
                                            vColor=color)
                
            self.glPoint(vP[0], vP[1], color)
            
    def glDrawPrimitives(self, vertexBuffer, vertexCount):
        for i in range(0, len(vertexBuffer), vertexCount * 3):
            v0 = vertexBuffer[i:i+3]
            v1 = vertexBuffer[i+3:i+6]
            v2 = vertexBuffer[i+6:i+9]
            
            A = [v0[0], v0[1], v0[2]]
            B = [v1[0], v1[1], v1[2]]
            C = [v2[0], v2[1], v2[2]]
            
            self.glTriangle(A, B, C)
