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
    u, v, w = kwargs["bCoords"]
    cA, cB, cC = kwargs["vertColors"]
    
    
    r = u*cA[0] + v*cB[0] + w*cC[0]
    g = u*cA[1] + v*cB[1] + w*cC[1]
    b = u*cA[2] + v*cB[2] + w*cC[2]
    return [r,g,b]