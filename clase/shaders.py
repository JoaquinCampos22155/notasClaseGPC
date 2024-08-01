from Mathlib import *
def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1.0]

    vt1 = matrix_vector_mult(modelMatrix, vt)

    vt2 = matrix_vector_mult(viewMatrix, vt1)

    vt_normalized = normalize(vt2)

    return vt_normalized