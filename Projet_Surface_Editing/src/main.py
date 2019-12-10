#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
import sys
from affichage import *
from minimization import *



def main():
    myMesh = Mesh()
    myMesh.parseEntry(sys.argv[1]) if len(sys.argv) > 1 else myMesh.parseEntry()
    #myMesh.draw()


    originIndex = 30
    # newPointPos = (0.1950900852680206, -1.600000023841858, 0.9807853102684021)
    newPointPos = (0.1950900852680206, -1.900000023841858, 0.9807853102684021)
    zone = IntrestZone(myMesh)
     # zone.findPointsBydistance(myMesh.points[0], 1)
    zone.findPointsByVoisins(originIndex, 1)
    # zone.draw()
    #print(myMesh.points[originIndex])
    #print(newPointPos)
    # mesLap = myMesh.computeLaplacianVertices()
    # delta = [mesLap[i][j] for i in zone.intrestPoints for j in range(3)] #on recupere que les lap de la zone d'interet comme x, y, z
    # x0 = [myMesh.points[i][j] for i in zone.intrestPoints for j in range(3)]
    # errorFonctional(x0, delta, myMesh, zone, originIndex, newPointPos)
    
    res = minimizationError(myMesh, zone, 30, newPointPos)
    
    for i in range(0, 3*len(zone.intrestPoints),3):
        myMesh.points[zone.intrestPoints[i//3]] = (res.x[i], res.x[i+1], res.x[i+2])

    affichage(myMesh, zone)
    #print(res.x)


main()
