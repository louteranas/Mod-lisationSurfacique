#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
import sys
from affichage import *
import numpy as np
from scipy.optimize import minimize

#https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html


def normeCarre(vertex):
    return (vertex[0]**2+vertex[1]**2+vertex[2]**2)


#surement à mettre dans IntrestZone
def errorFonctional(x):
    #delta c'est les Laplacien des points de la zone d'interet de départ des vi
    #un le point qu'on veut bouger
    #le computeLaplacienVertices doit surement être modifié pour ne prendre qu'un point en entrée
    #numeroPoint
    return (sum(normeCarre(delta[:] - computeLaplacienVertices(x[:]))) + normeCarre(x[numeroPoint]-un))

def minimizationError(monMesh, maZone, numeroPoint, nouveauPoint):
    #calcul de delta: point de la zone d'interet avant transformation en Laplacian
    mesLap = monMesh.computeLaplacianVertices(monMesh.points)
    delta = [mesLap[i] for i in maZone.indexPoints] #on recupere que les lap de la zone d'interet
