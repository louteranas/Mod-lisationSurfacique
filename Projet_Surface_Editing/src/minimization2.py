#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
import sys
from affichage import *
import numpy as np

import scipy

def minimization2(monMesh, maZone, originPointIndex, nouveauPoint):
    A = np.array(maZone.computeMatrixA())
    matriceMin = A.transpose().dot(A) #AtA
    bx, by, bz = maZone.delta()
    bx.append(nouveauPoint[0])
    by.append(nouveauPoint[1])
    bz.append(nouveauPoint[2])

    #point de depart de la resolution de ax=b :inutil
    vx = [monMesh.points[i][0] for i in maZone.intrestPoints]
    vy = [monMesh.points[i][1] for i in maZone.intrestPoints]
    vz = [monMesh.points[i][2] for i in maZone.intrestPoints]

    # essaie 1
    # xx = np.linalg.solve(matriceMin, A.transpose().dot(bx))
    # xy = np.linalg.solve(matriceMin, A.transpose().dot(by))
    # xz = np.linalg.solve(matriceMin, A.transpose().dot(bz))

    # essaie 2
    # xx = np.linalg.inv(A).dot(bx)
    # xy = np.linalg.inv(A).dot(by)
    # xz = np.linalg.inv(A).dot(bz)

    # essaie 3
    #P, L, U = scipy.linalg.lu(A)
    xx = scipy.linalg.solve(A, bx)
    xy = scipy.linalg.solve(A, by)
    xz = scipy.linalg.solve(A, bz)
    return [xx, xy, xz]
