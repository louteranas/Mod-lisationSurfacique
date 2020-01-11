#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
from amelioration import newB
import sys
from affichagePoor import *
import numpy as np

import scipy



def minimizationHandle(monMesh, maZone, originPointIndex, newListePointsHandle, boolTi=False, typeSolveur=True):
    "lance le calcule des nouveau points avec le mesh la ROI, le point centrale du handle,\
     la nouvelle possition des points du handle, un bool pour utiliser ou non les Ti, et un autre pour le choix du solveur (facultatif) "

    #créatiuon de la matrice A
    A = np.array(maZone.computeMatrixA(len(newListePointsHandle)))
    matriceMin = A.transpose().dot(A) #AtA

    #creation du vecteur b de la minimisation
    bx, by, bz = maZone.delta()
    #si demandé calcul b avec l'amélioration des Ti
    if boolTi == True:
        bx, by, bz = newB(monMesh, maZone, originPointIndex, newListePointsHandle[-1], bx, by, bz)
    #ajout de la fin des élements du b correspondant aux points du Handle
    for point in newListePointsHandle:
        bx.append(point[0])
        by.append(point[1])
        bz.append(point[2])

    #choix du solveur
    if typeSolveur == True:
        # solveur 1
        xx = np.linalg.solve(matriceMin, (A.transpose()).dot(bx))
        xy = np.linalg.solve(matriceMin, (A.transpose()).dot(by))
        xz = np.linalg.solve(matriceMin, (A.transpose()).dot(bz))
    else:
        # solveur 2
        xx = np.linalg.inv(matriceMin).dot(A.transpose().dot(bx))
        xy = np.linalg.inv(matriceMin).dot(A.transpose().dot(by))
        xz = np.linalg.inv(matriceMin).dot(A.transpose().dot(bz))

    return [xx, xy, xz]
