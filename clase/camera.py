from Mathlib import *

class Camera(object):
    def __init__(self):
        
        self.translate = [0,0,0]
        self.rotate = [0,0,0]
    
    #mult. de matriz
    def GetViewMatrix(self):
        translateMat = TranslationMatrix(self.translate[0],
                                         self.translate[1],
                                         self.translate[2])
        
        rotateMat = RotationMatrix(self.rotate[0],
                                         self.rotate[1],
                                         self.rotate[2])

        #camMatrix 
        camMatrix = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]]
        
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    camMatrix[i][j] += translateMat[i][k] * rotateMat[k][j]  
        
        #inversa de camMatrix
        camMatrixInv = inverseMatrix(camMatrix)
        return camMatrixInv 
