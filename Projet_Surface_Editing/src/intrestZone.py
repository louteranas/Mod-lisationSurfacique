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

    def computeDistance(self, originPoint, endPoint):
        return math.sqrt(pow(originPoint[0] - endPoint[0], 2) +\
                         pow(originPoint[1] - endPoint[1], 2) +\
                         pow(originPoint[2] - endPoint[2], 2))

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
        print(self.intrestPoints)

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
        for point in self.intrestPoints[:-1]:
            #matrix[k] = [self.originalMesh.adjacentMatrix[point] for point in self.intrestPoints]
            matrix.append([LaplaMatrix[point][e] for e in self.intrestPoints])
        lastLigne =[0 for _ in range(self.numberOfPoints-1)]
        lastLigne.append(1)
        #print(lastLigne)
        matrix.append(lastLigne)
        #print((matrix))
        return matrix

    #return delta x, y, z:le debut des vecteurs bx; by, bz defini dans le papier pour 1 SEUL point déplacé
    def delta(self):
        LaplacianVertices = self.originalMesh.computeLaplacianVertices()


        bx = [LaplacianVertices[e][0] for e in self.intrestPoints[:-1]]
        by = [LaplacianVertices[e][1] for e in self.intrestPoints[:-1]]
        bz = [LaplacianVertices[e][2] for e in self.intrestPoints[:-1]]
        return bx, by, bz








    def draw(self):
        print(self.intrestPoints)
