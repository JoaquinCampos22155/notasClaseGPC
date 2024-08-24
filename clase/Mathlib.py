from math import cos, sin, pi, isclose
import math
#operaciones de matrices
def normalize_vector(v):
    magnitude = math.sqrt(sum(x**2 for x in v))
    return [x / magnitude for x in v]
    
def normalize(vector):
    return [vector[0] / vector[3], vector[1] / vector[3], vector[2] / vector[3]]
def dotProd(vec1, vec2):
    # Asegúrate de que ambas listas tengan al menos 3 elementos
    if len(vec1) < 3:
        vec1 = vec1 + [0] * (3 - len(vec1))  # Rellena con ceros si es necesario
    if len(vec2) < 3:
        vec2 = vec2 + [0] * (3 - len(vec2))  # Rellena con ceros si es necesario
    
    # Calcula el producto punto
    x = vec1[0] * vec2[0]
    y = vec1[1] * vec2[1]
    z = vec1[2] * vec2[2]
    
    res = x + y + z
    return res
def crossProd(mat1, mat2):
    return [
        mat1[1] * mat2[2] - mat1[2] * mat2[1],  # Componente i (positivo)
        -(mat1[0] * mat2[2] - mat1[2] * mat2[0]),  # Componente j (negativo)
        mat1[0] * mat2[1] - mat1[1] * mat2[0]   # Componente k (positivo)
    ]

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

#matriz inversa
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

#coordenadas baricentricas
def barycentricCoords(A, B, C, P):
	
	# Se saca el �rea de los subtri�ngulos y del tri�ngulo
	# mayor usando el Shoelace Theorem, una f�rmula que permite
	# sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el �rea del tri�ngulo es 0, retornar nada para
	# prevenir divisi�n por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baric�ntricas dividiendo el 
	# �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC

	# Si cada coordenada est� entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son v�lidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None

#Render de clase 2 matrices de pos, tamaño y rotacion 
def TranslationMatrix(x, y, z):
    matrixT = [[1, 0, 0, x],
               [0, 1, 0, y],
               [0, 0, 1, z],
               [0, 0, 0, 1]]
    return matrixT

def toArray(vect):
    array = [] 
    for i in range(len(vect)):
        array.append(vect[i])
    return array

def ScaleMatrix(x, y, z):
    matrixS = [[x, 0, 0, 0],
               [0, y, 0, 0],
               [0, 0, z, 0],
               [0, 0, 0, 1]]
    return matrixS
def toList(array):
    if isinstance(array, (list, tuple)):  
        return [toList(item) for item in array]
    else: 
        return array

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

