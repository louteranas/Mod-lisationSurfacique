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

def normeCarrePoint(x, nouveauPoint):
    return ((x[-3]-nouveauPoint[0])**2 + (x[-2]-nouveauPoint[1])**2 + (x[-1]-nouveauPoint[2])**2)


#surement à mettre dans IntrestZone
def errorFonctional(x, delta, monMesh, maZone, originIndex, nouveauPoint):
    #delta c'est les Laplacian des points de la zone d'interet de départ des vi
    #un le point qu'on veut bouger
    #le computeLaplacianVertices doit surement être modifié pour ne prendre qu'un point en entrée
    #numeroPoint
    laplacianCoords = computeLaplacian(x, monMesh, maZone)
    # print(normeCarrePoint(x, nouveauPoint))
    # print((normeCarreList(delta, laplacianCoords) + normeCarrePoint(x, nouveauPoint)))
    return (normeCarreList(delta, laplacianCoords) + normeCarrePoint(x, nouveauPoint))

def computeLaplacian(x, monMesh, maZone):
    laplacianCoords = [0 for _ in range(3*len(maZone.intrestPoints))]
    for i in range(0, 3*len(maZone.intrestPoints), 3):
        index = maZone.intrestPoints[i//3] # index iterates the indexes that define the interest zone
        voisinsDeSomme = [monMesh.points[voisinIndex] for voisinIndex in monMesh.getFirstVoisins(index)]
        laplacianCoords[i] = monMesh.points[index][0]-(1/monMesh.degreeMatrix[index][index])*(sum([point[0] for point in voisinsDeSomme]))
        laplacianCoords[i+1] = monMesh.points[index][1]-(1/monMesh.degreeMatrix[index][index])*(sum([point[1] for point in voisinsDeSomme]))
        laplacianCoords[i+2] = monMesh.points[index][2]-(1/monMesh.degreeMatrix[index][index])*(sum([point[2] for point in voisinsDeSomme]))
    return laplacianCoords


def minimizationError(monMesh, maZone, originPointIndex, nouveauPoint):
    #calcul de delta: point de la zone d'interet avant transformation en Laplacian
    mesLap = monMesh.computeLaplacianVertices()
    delta = [mesLap[i][j] for i in maZone.intrestPoints for j in range(3)] #on recupere que les lap de la zone d'interet comme x, y, z
    x0 = [monMesh.points[i][j] for i in maZone.intrestPoints for j in range(3)]
    #print(x0)
    return minimize(errorFonctional, x0, args=(delta, monMesh, maZone, originPointIndex, nouveauPoint),method='nelder-mead',options={'xtol': 1e-8, 'disp': True})
