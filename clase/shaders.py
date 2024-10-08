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

def fragmentShader(**kwargs):
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