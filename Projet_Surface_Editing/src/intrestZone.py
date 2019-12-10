#!/usr/bin/env python3
from mesh import Mesh
import math
from itertools import *


class IntrestZone:
    def __init__(self, mesh):
        self.originalMesh = mesh
        self.numberOfPoints = 0
        self.intrestPoints = [] #list de points (copie des poins du mesh original)
        #il me faudrait les indices des points (plus utile que ce qu'il y a au dessus):
        self.indexPoints = []
        self.faces = [] #indices des face sur le mesh original

    def computeDistance(self, originPoint, endPoint):
        return math.sqrt(pow(originPoint[0] - endPoint[0], 2) +\
                         pow(originPoint[1] - endPoint[1], 2) +\
                         pow(originPoint[2] - endPoint[2], 2))

    def findPointsBydistance(self, origin, distance):
        for index, point in enumerate(self.originalMesh.points):
            if(self.computeDistance(origin, point) < distance):
                self.intrestPoints.append(point)
                self.indexPoints.append(index)
                self.getFacesInInterestZone(index)
                self.numberOfPoints += 1
        self.faces = list(set(self.faces))

    def findPointsByVoisins(self, origin, degree):
        self.intrestPoints = self.originalMesh.getAllVoisins(origin, degree)
        if(origin not in self.intrestPoints):
            self.intrestPoints.append(origin)
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


    def draw(self):
        print(self.intrestPoints)
