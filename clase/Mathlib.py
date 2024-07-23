from math import cos, sin, pi

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