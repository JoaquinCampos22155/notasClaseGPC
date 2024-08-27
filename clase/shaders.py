from Mathlib import *
import math
def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix= kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]


    vt = [vertex[0], vertex[1], vertex[2], 1]
    
    vt1 = matrixMult(viewportMatrix, projectionMatrix)
    vt11 = matrixMult(vt1, viewMatrix)
    vt111 = matrixMult(vt11, modelMatrix)
     
    vt2 = matrix_vector_mult(vt111, vt)

    vt = normalize(vt2)

    return vt

def unlitShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # sabiendo que los valores de las noramles estan en la 6,7,8 pos
    #guardamos 
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]
    

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    return [r,g,b]

def glowShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]
    camMatrix = kwargs["camMatrix"]
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # sabiendo que los valores de las noramles estan en la 6,7,8 pos
    #guardamos 
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v*nB[0] + w*nC[0],
              u * nA[1] + v*nB[1] + w*nC[1],
              u * nA[2] + v*nB[2] + w*nC[2]]
    
        
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]
    

    if len(textureList) > 0:
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
       
    #error? convertir dirLight to array 
    x = [-1 * elem for elem in toArray(dirLight)]
    intensity = dotProd(normal, x)
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    #Glow
    yellowGlow = [0.7, 0.4, 0.4]
    
    camForward = [camMatrix[0][2],  
              camMatrix[1][2],  
              camMatrix[2][2]]  
    
    glowIntesity = 1- dotProd(normal, camForward)
    glowIntesity = min(1, max(0, glowIntesity))
    r += yellowGlow[0] * glowIntesity
    g += yellowGlow[1] * glowIntesity
    b += yellowGlow[2] * glowIntesity
    
    
    return [min(1, r),
            min(1, g),
            min(1, b)]

def gouradShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # sabiendo que los valores de las noramles estan en la 6,7,8 pos
    #guardamos 
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v*nB[0] + w*nC[0],
              u * nA[1] + v*nB[1] + w*nC[1],
              u * nA[2] + v*nB[2] + w*nC[2],
              0]
    normal = matrix_vector_mult(modelMatrix, normal)
    normal = [-1 * elem for elem in toArray(normal)]
    normal = [normal[0], normal[1], normal[2]]
    normal = normalize_vector(normal)

    
        
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]

    if len(textureList) > 0:
        
        texColor = textureList[0].getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
       
    #error? convertir dirLight to array 
    x = [-1 * elem for elem in toArray(dirLight)]
    intensity = dotProd(normal, x)
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    return [r,g,b]

def textureBlendShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    textureList = kwargs["textureList"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # sabiendo que los valores de las noramles estan en la 6,7,8 pos
    #guardamos 
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v*nB[0] + w*nC[0],
              u * nA[1] + v*nB[1] + w*nC[1],
              u * nA[2] + v*nB[2] + w*nC[2],
              0]
    normal = matrix_vector_mult(modelMatrix, normal)
    normal = [-1 * elem for elem in toArray(normal)]
    normal = [normal[0], normal[1], normal[2]]
    normal = normalize_vector(normal)

    
        
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]
    
    x = [-1 * elem for elem in toArray(dirLight)]
    intensity = dotProd(normal, x)
    intensity = max(0, intensity)
    
    if len(textureList) >= 2:
        texColor1 = textureList[0].getColor(vtP[0], vtP[1])
        texColor2 = textureList[1].getColor(vtP[0], vtP[1])
        texColor3 = textureList[2].getColor(vtP[0], vtP[1])
        
        r *= (texColor1[0] * intensity) + (texColor2[0] * (1-intensity)) + (texColor3[0] * (1-intensity))
        g *= (texColor1[1] * intensity) + (texColor2[1] * (1-intensity)) + (texColor3[1] * (1-intensity))
        b *= (texColor1[2] * intensity) + (texColor2[2] * (1-intensity)) + (texColor3[2] * (1-intensity))
    
    return [r,g,b]
def flatShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    # sabiendo que los valores de las noramles estan en la 6,7,8 pos
    # guardamos 
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
        
    normal = [(nA[0] +nB[0] +nC[0])/3,
              (nA[1] +nB[1] +nC[1])/3,
              (nA[2] +nB[2] +nC[2])/3]
    
        
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]
    

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
       
    x = [-1 * elem for elem in toArray(dirLight)]
    intensity = dotProd(normal, x)
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    return [r,g,b]

def toonShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # sabiendo que los valores de las noramles estan en la 6,7,8 pos
    #guardamos 
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v*nB[0] + w*nC[0],
              u * nA[1] + v*nB[1] + w*nC[1],
              u * nA[2] + v*nB[2] + w*nC[2]]
    
        
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]
    

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
       
    #error? convertir dirLight to array 
    x = [-1 * elem for elem in toArray(dirLight)]
    intensity = dotProd(normal, x)
    intensity = max(0, intensity)
    
    if intensity <0.33:
        intensity = 0.3
    elif intensity <0.66:
        intensity = 0.6
    else:
        intensity = 1
    
    r *= intensity
    g *= intensity
    b *= intensity
    
    return [r,g,b]


def bywshader(**kwargs):
    # por píxel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]
    dirLight2 = kwargs["dirLight2"]  

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]

    magnitude = math.sqrt(sum(x**2 for x in normal))
    normal = [x / magnitude for x in normal]

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    x_coord = vtP[0] % 1.0  

    stripe_width = 0.1  
    if (x_coord // stripe_width) % 2 == 0:
        baseColor = [1.0, 1.0, 1.0]  
    else:
        baseColor = [0.9, 0.9, 0.9]  

    dirLight = toArray(dirLight)
    dirLight2 = toArray(dirLight2)
    
    x1 = [-d for d in dirLight]  
    intensity1 = dotProd(normal, x1)
    
    x2 = [-d for d in dirLight2] 
    intensity2 = dotProd(normal, x2)

    intensity = max(0, intensity1) + max(0, intensity2)
    intensity = min(intensity, 1)  

    r = baseColor[0] * intensity
    g = baseColor[1] * intensity
    b = baseColor[2] * intensity
    
    r = max(0, min(r, 1))
    g = max(0, min(g, 1))
    b = max(0, min(b, 1))
    
    return [r, g, b]

def edgesgreenShader(**kwargs):
    # Por píxel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]
    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # Calcular la posición de textura
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    def distanceToEdge(p, a, b):
        return abs((b[1] - a[1]) * p[0] - (b[0] - a[0]) * p[1] + b[0] * a[1] - b[1] * a[0]) / math.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2)
    
    edgeThreshold = 0.05  
    
    distA_B = distanceToEdge(vtP, vtA, vtB)
    distB_C = distanceToEdge(vtP, vtB, vtC)
    distC_A = distanceToEdge(vtP, vtC, vtA)
    
    if distA_B < edgeThreshold or distB_C < edgeThreshold or distC_A < edgeThreshold:
        return [0, 1, 0] 
    else:
        return [0, 0, 0]  
    
def lineShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]
    

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    height = u * A[1] + v *B[1] + w * C[1]
    valuey = sin(height)
    if valuey < 0.5:
        return None
    return [r,g,b]

def waffleShader(**kwargs):
    #por pixel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    
    r = 1
    g = 1
    b = 1
    
    
    vtP = [ u * vtA[0] + v *vtB[0] + w * vtC[0],
            u * vtA[1] + v *vtB[1] + w * vtC[1]]
    

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    height = u * A[1] + v *B[1] + w * C[1]
    width = u * A[0] + v *B[0] + w * C[0]
    valuey = sin(height)
    valuex = sin(width)
    if valuex < 0.5 and valuey <0.5:
        return None
    return [r,g,b]
def majoraskShader(**kwargs):
    # por píxel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs["textureList"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    # Sabemos que los valores de las normales están en la 6, 7, 8 posición
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    magnitude = math.sqrt(sum(x**2 for x in normal))
    normal = [x / magnitude for x in normal]

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    baseColor = [0.5, 0.5, 1.0]  

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        baseColor = [baseColor[i] * texColor[i] for i in range(3)]

    dirLight = toArray(dirLight)
    
    x = -1*dirLight
    intensity = dotProd(normal, x)
    intensity = max(0, intensity)
    
    r = baseColor[0] * intensity + 0.2 * math.sin(normal[0] * 10)
    g = baseColor[1] * intensity + 0.2 * math.sin(normal[1] * 10)
    b = baseColor[2] * intensity + 0.2 * math.sin(normal[2] * 10)
    
    r = max(0, min(r, 1))
    g = max(0, min(g, 1))
    b = max(0, min(b, 1))
    
    return [r, g, b]
