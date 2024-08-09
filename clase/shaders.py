from Mathlib import *
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