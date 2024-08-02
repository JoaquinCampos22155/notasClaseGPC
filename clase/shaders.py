def matrix_vector_mult(matrix, vector):
    """ Multiplica una matriz 4x4 por un vector 4x1 """
    result = [0, 0, 0, 0]
    for i in range(4):
        result[i] = sum(matrix[i][j] * vector[j] for j in range(4))
    return result

def vertexShader(vertex, **kwargs):
    # para cada vertice
    modelMatrix = kwargs["modelMatrix"]
    
    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]
    
    vt = matrix_vector_mult(modelMatrix, vt)
    
    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]
    
    return vt

<<<<<<< Updated upstream
# Ejemplo de uso
modelMatrix = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

vertex = [1, 2, 3]

print(vertexShader(vertex, modelMatrix=modelMatrix))
=======
    vt = [vertex[0], vertex[1], vertex[2], 1]
    
    vt1 = matrixMult(viewportMatrix, projectionMatrix)
    vt11 = matrixMult(vt1, viewMatrix)
    vt111 = matrixMult(vt11, modelMatrix)
     
    vt2 = matrix_vector_mult(vt111, vt)

    vt = normalize(vt2)

    return vt
>>>>>>> Stashed changes
