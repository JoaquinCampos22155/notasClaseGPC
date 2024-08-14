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

def gouradShader(**kwargs):
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
    r *= intensity
    g *= intensity
    b *= intensity
    
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


def majoraskShader(**kwargs):
    # por píxel
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
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