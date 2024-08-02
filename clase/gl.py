import struct 
import model as model
def char(c):
    #1 byte
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    #2 bytes
    return struct.pack("=h", w)

def dword(d):
    #4 bytes
    return struct.pack("=l", d)

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()
    
        self.vertexShader = None
        
        self.models = []
        
<<<<<<< Updated upstream
=======
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
        
         
>>>>>>> Stashed changes
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
                    v0 = self.vertexShader(v0, modelMatrix = mMat)
                    v1 = self.vertexShader(v1, modelMatrix = mMat)
                    v2 = self.vertexShader(v2, modelMatrix = mMat)
                    if vertCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix = mMat)
                    
                    
                    
                self.glPoint(int(v0[0]), int(v0[1]))
                self.glPoint(int(v1[0]), int(v1[1]))
                self.glPoint(int(v2[0]), int(v2[1]))
                if vertCount == 4:
<<<<<<< Updated upstream
                    self.glPoint(int(v3[0]), int(v3[1]))
=======
                    vertexBuffer.append(v0)
                    vertexBuffer.append(v2)
                    vertexBuffer.append(v3)
                    
            self.glDrawPrimitives(vertexBuffer)
                    
            
    def glTriangle(self, A, B, C , color = None):
        if  A[1]<B[1]:
            A, B = B, A
        if A[1] <C[1]:
            A,C = C, A
        if B[1] <C[1]:
            B,C = C,B
        self.glLine((A[0], A[1]),(B[0], B[1]))
        self.glLine((B[0], B[1]),(C[0], C[1]))
        self.glLine((C[0], C[1]),(A[0], A[1]))
        
        if B[1] == C[1]:
            #parte plana abajo 
        
    def glDrawPrimitives(self, buffer):
        if self.primitiveType == POINTS:
                for point in buffer:
                    self.glPoint(int(point[0]), int(point[1]))
        elif self.primitiveType == LINES:
            for i in range(0, len(buffer), 3):
                p0 = buffer[i]
                p1 = buffer[i+1]
                p2 = buffer[i+2]
>>>>>>> Stashed changes
                
                self.glLine((v0[0], v0[1]),(v1[0], v1[1]))
                self.glLine((v1[0], v1[1]),(v2[0], v2[1]))
                self.glLine((v2[0], v2[1]),(v0[0], v0[1]))
                if vertCount == 4:
                    self.glLine((v0[0], v0[1]),(v2[0], v2[1]))
                    self.glLine((v2[0], v2[1]),(v3[0], v3[1]))
                    self.glLine((v3[0], v3[1]),(v0[0], v0[1]))
                    