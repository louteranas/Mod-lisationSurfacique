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

    def reset(self):
        self.numberOfPoints = 0
        self.intrestPoints = [] #list d'indice points (copie des poins du mesh original)
        self.faces = [] #indices des face sur le mesh original
        self.dictFaces = {}

#Fonctions utiles pour la création de la ROI par distance et non par voisinnage

    def computeDistance(self, originPoint, endPoint):
        "renvoie la distance entre 2 points en donnant leur indice"
        return math.sqrt(pow(originPoint[0] - endPoint[0], 2) +\
                         pow(originPoint[1] - endPoint[1], 2) +\
                         pow(originPoint[2] - endPoint[2], 2))

    def findPointsBydistance(self, origin, distance):
        "creer la ROI par distance"
        for index, point in enumerate(self.originalMesh.points):
            if(self.computeDistance(origin, point) < distance):
                self.intrestPoints.append(point)
                self.getFacesInInterestZone(index)
                self.numberOfPoints += 1
        self.faces = list(set(self.faces))

#Fonctions utiles pour la création de la ROI par voisinnage

    def findPointsByVoisins(self, origin, degree):
        "creer la zone d'interet autour de l'origine avec distande degree"
        self.intrestPoints = self.originalMesh.getAllVoisins(origin, degree)
        if(origin in self.intrestPoints):
            self.intrestPoints.remove(origin)
        self.intrestPoints.append(origin) # i force the origin point to be the last index in interest zone
        for index in self.intrestPoints:
            self.getFacesInInterestZone(index)
        self.numberOfPoints = len(self.intrestPoints)
        self.faces = list(set(self.faces))


    def getFacesInInterestZone(self, vertexIndex):
        "retourne les faces de la ROI pour l'affichage du début ave Pygame qui fonctionne à l'ensimagw"
        for face in self.originalMesh.facesIndexs:
            if(vertexIndex in face):
                index = face.index(vertexIndex)
                goodFace = True
                for i in range(3):
                    if i != index and not(face[i] in self.intrestPoints):
                        goodFace = False
                if goodFace:
                    self.faces.append(face)


#Fonction utiles pour le solveur

    def computeMatrixA(self, nbPointsHandle=1):
        "return Matrice A de à minimiser definie dans le papier"
        matrix = []
        LaplaMatrix = self.originalMesh.computeLaplacianMatrix()
        for point in self.intrestPoints:
            matrix.append([LaplaMatrix[point][e] for e in self.intrestPoints])
        lastLigne =[0 for _ in range(self.numberOfPoints-nbPointsHandle)]
        for i in range(nbPointsHandle):
            ligneMatrixI = [0] * nbPointsHandle
            ligneMatrixI[i] = 1
            matrix.append(lastLigne+ligneMatrixI)
        return matrix

    def delta(self):
        "calcule les coordonnées laplaciennes pour la ROI, utilisées pour le b de la minimisation"
        box =[self.originalMesh.points[e][0] for e in self.intrestPoints]
        boy =[self.originalMesh.points[e][1] for e in self.intrestPoints]
        boz =[self.originalMesh.points[e][2] for e in self.intrestPoints]
        A = np.array(self.computeMatrixA())[:-1]
        bx = list(A.dot(box))
        by = list(A.dot(boy))
        bz = list(A.dot(boz))
        return bx, by, bz

#Pour l'affichage de la zone

    def getPositions(self):
        "renvoie les positions de la zone"
        output = []
        compteur = 0
        for vertexIndex in self.intrestPoints:
            self.dictFaces[vertexIndex] = compteur
            for coord in self.originalMesh.points[vertexIndex]:
                output.append(float(coord))
            compteur += 1
        return tuple(output)

    def getFaces(self):
        "renvoie les face de la zone pour l'affichage"
        output = []
        for face in self.faces:
            goodFace =True
            for index in face:
                if(index not in self.intrestPoints):
                    goodFace = False
            if(goodFace):
                for index in face:
                    output.append(self.dictFaces[index])
        return output
