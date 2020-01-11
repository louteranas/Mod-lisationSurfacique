#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
from amelioration import newB
import sys
from affichage import *
import numpy as np

import scipy

def minimization2(monMesh, maZone, originPointIndex, nouveauPoint, boolTi, typeSolveur=1):
    A = np.array(maZone.computeMatrixA())
    matriceMin = A.transpose().dot(A) #AtA
    #bx, by, bz = maZone.delta()
    if boolTi ==False:
        bx, by, bz = maZone.delta2()
    else:
        bx, by, bz = newB(monMesh, maZone, originPointIndex, nouveauPoint, bx, by, bz)
    bx.append(nouveauPoint[0])
    by.append(nouveauPoint[1])
    bz.append(nouveauPoint[2])



    #choix du solveur
    if typeSolveur == 1:
        # solveur 1
        xx = np.linalg.solve(matriceMin, (A.transpose()).dot(bx))
        xy = np.linalg.solve(matriceMin, (A.transpose()).dot(by))
        xz = np.linalg.solve(matriceMin, (A.transpose()).dot(bz))
    elif typeSolveur == 2:
        # solveur 2
        xx = np.linalg.inv(matriceMin).dot(A.transpose().dot(bx))
        xy = np.linalg.inv(matriceMin).dot(A.transpose().dot(by))
        xz = np.linalg.inv(matriceMin).dot(A.transpose().dot(bz))
    else:
        # solveur 3
        xx = scipy.linalg.solve(A, bx)
        xy = scipy.linalg.solve(A, by)
        xz = scipy.linalg.solve(A, bz)
        
    return [xx, xy, xz]
