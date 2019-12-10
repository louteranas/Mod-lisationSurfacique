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



    zone = IntrestZone(myMesh)
     # zone.findPointsBydistance(myMesh.points[0], 1)
    zone.findPointsByVoisins(30, 1)
    # zone.draw()
    #affichage(myMesh, zone)
    res = minimizationError(myMesh, zone, 30, (10,10,8))


main()
