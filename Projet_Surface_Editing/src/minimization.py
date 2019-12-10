#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
import sys
from affichage import *
import numpy as np
from scipy.optimize import minimize

#https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html


def normeCarreList(delta, laplacient):
    return sum([(delta[i] - laplacient[i])**2 for i in range(0, len(laplacient))])

def normeCarrePoint(x, index, nouveauPoint):
    return ((x[3*index][0]-nouveauPoint[0])**2 + (x[3*index][1]-nouveauPoint[1])**2 + (x[3*index][2]-nouveauPoint[2])**2)


#surement à mettre dans IntrestZone
def errorFonctional(delta, x, monMesh, maZone, originIndex, nouveauPoint):
    #delta c'est les Laplacien des points de la zone d'interet de départ des vi
    #un le point qu'on veut bouger
    #le computeLaplacienVertices doit surement être modifié pour ne prendre qu'un point en entrée
    #numeroPoint
    laplacientCoords = computeLaplacient(x, monMesh, maZone)
    return (normeCarreList(delta, laplacientCoords) + normeCarrePoint(x, originIndex, nouveauPoint))

def computeLaplacient(x, monMesh, maZone):
    laplacientCoords = [0 for _ in range(3*len(maZone.interestPoints))]
    for i in range(0, 3*len(maZone.interestPoints), 3):
        index = maZone.interestPoints[i//3]
        laplacientCoords[i] = monMesh.points[index][0]-(1/monMesh.degreeMatrix[index])*(sum([monMesh.points[voisinIndex][0] for voisinIndex in maZone.getFirstVoisins(index)]))
        laplacientCoords[i+1] = monMesh.points[index][1]-(1/monMesh.degreeMatrix[index])*(sum([monMesh.points[voisinIndex][1] for voisinIndex in maZone.getFirstVoisins(index)]))
        laplacientCoords[i+2] = monMesh.points[index][2]-(1/monMesh.degreeMatrix[index])*(sum([monMesh.points[voisinIndex][2] for voisinIndex in maZone.getFirstVoisins(index)]))
    return laplacientCoords


def minimizationError(monMesh, maZone, numeroPoint, nouveauPoint):
    #calcul de delta: point de la zone d'interet avant transformation en Laplacian
    mesLap = monMesh.computeLaplacianVertices()
    delta = [mesLap[i][j] for i in maZone.interestPoints for j in range(3)] #on recupere que les lap de la zone d'interet comme x, y, z
    x0 = [monMesh.points[i][j] for i in maZone.interestPoints for j in range(3)]
