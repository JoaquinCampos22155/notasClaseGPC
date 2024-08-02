from math import cos, sin, pi
def normalize(vector):
    return [vector[0] / vector[3], vector[1] / vector[3], vector[2] / vector[3]]

#mult elemento por elemento
def multExE(mat1, mat2):
    if not isinstance(mat2[0], list): 
        mat2 = [mat2 for _ in range(4)]

    result = [[mat1[i][j] * mat2[i][j] for j in range(4)] for i in range(4)]
    return result
#mult matriz vector
def matrix_vector_mult(matrix, vector):
    result = [0, 0, 0, 0]
    for i in range(4):
        result[i] = sum(matrix[i][j] * vector[j] for j in range(4))
    return result

#matriz 4x4 mult 
def matrixMult(matrix1, matrix2):
    result = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

    for i in range(4):
        for j in range(4):
            result[i][j] = matrix1[i][0] * matrix2[0][j] + matrix1[i][1] * matrix2[1][j] + matrix1[i][2] * matrix2[2][j] + matrix1[i][3] * matrix2[3][j]
    return result


def inverseMatrix(matrix):
    
    n = 4
    mat = [row[:] for row in matrix]
    identity = [[float(i == j) for j in range(n)] for i in range(n)]

    #GJ
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(mat[k][i]) > abs(mat[max_row][i]):
                max_row = k

        mat[i], mat[max_row] = mat[max_row], mat[i]
        identity[i], identity[max_row] = identity[max_row], identity[i]

        pivot = mat[i][i]
        if pivot == 0:
            return None  

        for j in range(n):
            mat[i][j] /= pivot
            identity[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = mat[k][i]
                for j in range(n):
                    mat[k][j] -= factor * mat[i][j]
                    identity[k][j] -= factor * identity[i][j]
    return identity

#Render de clase 2 matrices de pos, tamaño y rotacion 

def TranslationMatrix(x, y, z):
    matrixT = [[1, 0, 0, x],
               [0, 1, 0, y],
               [0, 0, 1, z],
               [0, 0, 0, 1]]
    return matrixT

def ScaleMatrix(x, y, z):
    matrixS = [[x, 0, 0, 0],
               [0, y, 0, 0],
               [0, 0, z, 0],
               [0, 0, 0, 1]]
    return matrixS

def RotationMatrix(pitch, yaw, roll):
    pitch *= pi / 180
    yaw *= pi / 180
    roll *= pi / 180
    
    pitchMat = [[1, 0, 0, 0],
                [0, cos(pitch), -sin(pitch), 0],
                [0, sin(pitch), cos(pitch), 0],
                [0, 0, 0, 1]]
    
    yawMat = [[cos(yaw), 0, sin(yaw), 0],
              [0, 1, 0, 0],
              [-sin(yaw), 0, cos(yaw), 0],
              [0, 0, 0, 1]]
    
    rollMat = [[cos(roll), -sin(roll), 0, 0],
               [sin(roll), cos(roll), 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]
    
    resultM = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
    
    intermediateM = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
    
    for i in range(4):
        for j in range(4):
            for k in range(4):
                intermediateM[i][j] += pitchMat[i][k] * yawMat[k][j]
    
    for i in range(4):
        for j in range(4):
            for k in range(4):
                resultM[i][j] += intermediateM[i][k] * rollMat[k][j]
    
    return resultM