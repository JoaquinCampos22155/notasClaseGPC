from Mathlib import *
def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix= kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    #vt = [vertex[0], vertex[1], vertex[2], 1.0]
    vt1 = matrix_vector_mult(viewportMatrix, projectionMatrix)
    vt11 = matrix_vector_mult(vt1, viewMatrix)
    vt111 = matrix_vector_mult(vt11, modelMatrix)

    vt_normalized = normalize(vt111)

    return vt_normalized