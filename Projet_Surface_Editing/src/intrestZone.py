#!/usr/bin/env python3
from mesh import Mesh
import math
import numpy as np
from itertools import *


class IntrestZone:
    def __init__(self, mesh):
        self.originalMesh = mesh
        self.numberOfPoints = 0
        self.intrestPoints = [] #list d'indice points (copie des poins du mesh original)
        self.faces = [] #indices des face sur le mesh original
        self.dictFaces = {}

    def computeDistance(self, originPoint, endPoint):
        return math.sqrt(pow(originPoint[0] - endPoint[0], 2) +\
                         pow(originPoint[1] - endPoint[1], 2) +\
                         pow(originPoint[2] - endPoint[2], 2))

    def reset(self):
        self.numberOfPoints = 0
        self.intrestPoints = [] #list d'indice points (copie des poins du mesh original)
        self.faces = [] #indices des face sur le mesh original
        self.dictFaces = {}
    
    def findPointsBydistance(self, origin, distance):
        for index, point in enumerate(self.originalMesh.points):
            if(self.computeDistance(origin, point) < distance):
                self.intrestPoints.append(point)
                self.getFacesInInterestZone(index)
                self.numberOfPoints += 1
        self.faces = list(set(self.faces))

    #creer la zone d'interet autour de l'origine avec distande degree
    def findPointsByVoisins(self, origin, degree):
        self.intrestPoints = self.originalMesh.getAllVoisins(origin, degree)
        if(origin in self.intrestPoints):
            self.intrestPoints.remove(origin)
        self.intrestPoints.append(origin) # i force the origin point to be the last index in interest zone
        #print(self.intrestPoints)

        for index in self.intrestPoints:
            self.getFacesInInterestZone(index)
        self.numberOfPoints = len(self.intrestPoints)
        self.faces = list(set(self.faces))


    def getFacesInInterestZone(self, vertexIndex):
        for face in self.originalMesh.facesIndexs:
            if(vertexIndex in face):
                index = face.index(vertexIndex)
                goodFace = True
                for i in range(3):
                    if i != index and not(face[i] in self.intrestPoints):
                        goodFace = False
                if goodFace:
                    self.faces.append(face)

    #return Matrice defini dans le papier pour 1 SEUL point déplacé
    def computeMatrixA(self):
        #matrix = np.identity(self.numberOfPoints)
        matrix = []
        LaplaMatrix = self.originalMesh.computeLaplacianMatrix()
        for point in self.intrestPoints:
        #for point in self.intrestPoints[:-1]:
            #matrix[k] = [self.originalMesh.adjacentMatrix[point] for point in self.intrestPoints]
            matrix.append([LaplaMatrix[point][e] for e in self.intrestPoints])
        lastLigne =[0 for _ in range(self.numberOfPoints-1)]
        lastLigne.append(1)
        #print(lastLigne)
        matrix.append(lastLigne)
        #print("taille matrix ", len(matrix), len(matrix[0]))
        #print("matrix: ", matrix)

        return matrix

    #return delta x, y, z:le debut des vecteurs bx; by, bz defini dans le papier pour 1 SEUL point déplacé
    def delta(self):
        LaplacianVertices = self.originalMesh.computeLaplacianVertices()

        box =[self.originalMesh.points[e][0] for e in self.intrestPoints[:-1]]
        boy =[self.originalMesh.points[e][1] for e in self.intrestPoints[:-1]]
        boz =[self.originalMesh.points[e][2] for e in self.intrestPoints[:-1]]

        bx = [LaplacianVertices[e][0] for e in self.intrestPoints]
        by = [LaplacianVertices[e][1] for e in self.intrestPoints]
        bz = [LaplacianVertices[e][2] for e in self.intrestPoints]
        # print("bx ", box, bx, "\n")
        # print("by ", boy, by, "\n")
        # print("bz ", boz, bz, "\n")
        return bx, by, bz

    def delta2(self):
        box =[self.originalMesh.points[e][0] for e in self.intrestPoints]
        boy =[self.originalMesh.points[e][1] for e in self.intrestPoints]
        boz =[self.originalMesh.points[e][2] for e in self.intrestPoints]
        A = np.array(self.computeMatrixA())[:-1]
        bx = list(A.dot(box))
        by = list(A.dot(boy))
        bz = list(A.dot(boz))

        return bx, by, bz
    
    def getPositions(self):
        output = []
        compteur = 0
        # print("poistions indexs = " + str(self.intrestPoints))
        for vertexIndex in self.intrestPoints:
            self.dictFaces[vertexIndex] = compteur
            for coord in self.originalMesh.points[vertexIndex]:    
                output.append(float(coord))
            compteur += 1
        # print(self.dictFaces)
        return tuple(output)
    
    def getFaces(self):
        output = []
        for face in self.faces:
            goodFace =True
            for index in face:
                if(index not in self.intrestPoints):
                    goodFace = False
            if(goodFace):
                for index in face:    
                    output.append(self.dictFaces[index])
        # for i in range(len(output)):
        #     output[i] =
        # print("faces = " + str(output))
        return output








    def draw(self):
        print(self.intrestPoints)
