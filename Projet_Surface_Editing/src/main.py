#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
import sys
#from affichage import *
from minimization import *
from minimization2 import *
import os



def main():
    myMesh = Mesh()

    myMesh.parseEntry(sys.argv[1]) if len(sys.argv) > 1 else myMesh.parseEntry()
    baseMeshPath = sys.argv[1] if len(sys.argv) > 1 else "../models/cylindre.off"
    #myMesh.draw()


    originIndex = 30
    # newPointPos = (0.1950900852680206, -1.600000023841858, 0.9807853102684021)

    newPointPos = (myMesh.points[originIndex][0]+0.5, myMesh.points[originIndex][1]-0.1, myMesh.points[originIndex][2])
    zone = IntrestZone(myMesh)
     # zone.findPointsBydistance(myMesh.points[0], 1)
    zone.findPointsByVoisins(originIndex,4)
    #zone.computeMatrixA()

    # zone.draw()
    #print(myMesh.points[originIndex])
    #print(newPointPos)
    # mesLap = myMesh.computeLaplacianVertices()
    # delta = [mesLap[i][j] for i in zone.intrestPoints for j in range(3)] #on recupere que les lap de la zone d'interet comme x, y, z
    # x0 = [myMesh.points[i][j] for i in zone.intrestPoints for j in range(3)]
    # errorFonctional(x0, delta, myMesh, zone, originIndex, newPointPos)

    #ancien
    #res = minimizationError(myMesh, zone, originIndex, newPointPos)
    #for i in range(0, 3*len(zone.intrestPoints),3):
    #    myMesh.points[zone.intrestPoints[i//3]] = (res.x[i], res.x[i+1], res.x[i+2])
    #fin ancien

    #affichage(myMesh, zone)
    #print(res.x)

    #myMesh.saveMeshOff()
    #os.system("meshlab " + baseMeshPath + " ../models/result_test.off &")
    #os.system("meshlab ../models/result_test.off &")

    #new
    res = minimization2(myMesh, zone, originIndex, newPointPos)
    for i in range(zone.numberOfPoints):
        myMesh.points[zone.intrestPoints[i]] = (res[0][i], res[1][i], res[2][i])
    myMesh.saveMeshOff()

main()
