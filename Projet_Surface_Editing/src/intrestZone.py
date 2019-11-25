#!/usr/bin/env python3
from mesh import Mesh
import math


class IntrestZone:
    def __init__(self, mesh):
        self.originalMesh = mesh 
        self.numberOfPoints = 0
        self.intrestPoints = []

    def computeDistance(self, originPoint, endPoint):
        return math.sqrt(pow(originPoint[0] - endPoint[0], 2) +\
                         pow(originPoint[1] - endPoint[1], 2) +\
                         pow(originPoint[2] - endPoint[2], 2))

    def findPointsBydistance(self, origin, distance):
        for point in self.originalMesh.points:
            if(self.computeDistance(origin, point) < distance):
                self.intrestPoints.append(point)
                numberOfPoints += 1

    def draw(self):
        print(self.numberOfPoints)
