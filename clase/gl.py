import struct 
from camera import Camera
from math import tan, pi, isclose
from Mathlib import barycentricCoords
from texture import Texture

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
    
        self.activeVertexShader = None
        self.activeFragmentShader = None
        self.activeModelMatrix = None


        self.directionalLight = [1,0,0]
        self.directionalLight2 = [0,1,1]
        self.activeTexture = None
        self.activeTextureList = None
        
        self.primitiveType = TRIANGLES
        
        self.models = []
        self.background = None
        
        
    def glLoadBackground(self, filename):
        self.background = Texture(filename)
    def glClearBackground(self):
        if self.background == None:
            return
        for x in range(self.vpX, self.vpX+self.vpwidth +1):
            for y in range(self.vpY, self.vpY+self.vpheight +1):
                tU = (x-self.vpX)/self.vpwidth
                tV = (y-self.vpY)/self.vpheight 
                texColor = self.background.getColor(tU, tV)
                if texColor:
                    self.glPoint(x, y, texColor)
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
        
        x = round(x)
        y = round(y)
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
            
            self.activeModelMatrix = model.GetModelMatrix()
            #guardar referencia de textura del modelo
            self.activeTexture = model.texture
            self.activeTextureList = model.textureList
            self.activeVertexShader = model.vertexShader
            self.activeFragmentShader = model.fragmentShader
            
            vertexBuffer = []
            
            for face in model.faces:
                faceVerts = []
                for i in range(len(face)):
                    vert = []
                    pos = model.vertices[face[i][0] - 1]
                    
                    if self.activeVertexShader:
                        pos = self.activeVertexShader(pos,
                                                modelMatrix=self.activeModelMatrix,
                                                viewMatrix=self.camera.GetViewMatrix(),
                                                projectionMatrix=self.projectionMatrix,
                                                viewportMatrix=self.viewportMatrix)
                    
                    for value in pos:
                        vert.append(value)
                        
                    #obtenemos coordenadas de textura
                    vts = model.texCoords[face[i][1] -1]
                    #agregando valores del vts al contenedor del vertice
                    for value in vts:
                        vert.append(value)
                    
                    #obtenemos las noramles de la cara actual
                    normal= model.normals[face[i][2] -1]
                    for value in normal:
                        vert.append(value)
                            
                    faceVerts.append(vert)
                
                for value in faceVerts[0]: vertexBuffer.append(value)
                for value in faceVerts[1]: vertexBuffer.append(value)
                for value in faceVerts[2]: vertexBuffer.append(value)
                if len(faceVerts) == 4:
                    for value in faceVerts[0]: vertexBuffer.append(value)
                    for value in faceVerts[2]: vertexBuffer.append(value)
                    for value in faceVerts[3]: vertexBuffer.append(value)

            self.glDrawPrimitives(vertexBuffer, 8)

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
            D = [A[0] + ((B[1] - A[1]) / (C[1] - A[1])) * (C[0] - A[0]), B[1]]
            
            u, v, w = barycentricCoords(A, B, C, D)
            for i in range(2,len(A)):
                
                D.append(u * A[i] + v *B[i] + w * C[i])
            flatBottom(A, B, D)
            flatTop(D, B, C)
    
    #funcion para dibujar triangulos sin hoyos   
    def glTriangle_bc(self, A, B, C):
        minX = round(min(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxX = round(max(A[0], B[0], C[0]))
        maxY = round(max(A[1], B[1], C[1]))
        
        for x in range(minX, maxX +1):
            for y in range(minY, maxY +1):
                P = [x,y]
                if barycentricCoords(A, B, C, P) != None:
                    self.glDrawTrianglePoint(A, B, C, P)
            
    def glDrawTrianglePoint(self, A, B, C, P):
        x = P[0]
        y = P[1]
        if not (0 <= x< self.width) or not (0 <= y <self.height):
            return
        
        
        bCoords = barycentricCoords(A, B, C, P)
        
        if bCoords == None:
            return
        
        u,v,w = bCoords
        
        # Hay que asaegurarse que coordsbari es igual a 1
        if not isclose(u+v+w, 1.0):
            return
        
        #se calcula valor de z
        z = u * A[2] + v * B[2] + w * C[2]
        #si el valor de z es mayor de el valor guardado en zbuffer esta mas lejos 
        if z >= self.zbuffer[x][y]:
            return
        if z < -1 or z > 1:
            return 
        self.zbuffer[x][y] = z
        
        color = self.currColor    
        if self.activeFragmentShader != None:
            verts = (A, B, C)
            color = self.activeFragmentShader(verts = verts, 
                                        bCoords = bCoords,
                                        texture = self.activeTexture,
                                        textureList = self.activeTextureList, 
                                        dirLight = self.directionalLight,
                                        dirLight2 = self.directionalLight2,
                                        camPosition = self.camera.translate,
                                        camMatrix = self.camera.GetViewMatrix(),
                                        modelMatrix = self.activeModelMatrix)
        if color != None:          
            self.glPoint(x, y, color)
            
    def glDrawPrimitives(self, buffer, vertexOffset):
        if self.primitiveType == POINTS:
            for i in range(0, len(buffer), vertexOffset):
                x = buffer[i]
                y = buffer[i + 1]
                self.glPoint(x, y)
        elif self.primitiveType == LINES:
            for i in range(0, len(buffer), vertexOffset *3):
                for j in range (3):
                    x0 = buffer[i+vertexOffset*j+0]
                    y0 = buffer[i+vertexOffset*j+1]

                    x1 = buffer[ i + vertexOffset * ((j + 1)%3) + 0]
                    y1 = buffer[ i + vertexOffset * ((j + 1)%3) + 1]
                    
                    self.glLine((x0,y0),(x1,y1))
        elif self.primitiveType == TRIANGLES:
            for i in range(0, len(buffer), vertexOffset * 3):    
                A = [ buffer[i + j + vertexOffset * 0] for j in range(vertexOffset)]
                B = [ buffer[i + j + vertexOffset * 1] for j in range(vertexOffset)]
                C = [ buffer[i + j + vertexOffset * 2] for j in range(vertexOffset)]
                
                self.glTriangle(A,B,C)
                
                