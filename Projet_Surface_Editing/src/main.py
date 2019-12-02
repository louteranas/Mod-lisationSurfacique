#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
import sys
from affichage import *



def main():
    myMesh = Mesh()
    myMesh.parseEntry(sys.argv[1])
    #myMesh.draw()



    zone = IntrestZone(myMesh)
    #zone.findPointsBydistance(myMesh.points[0], 1)
    zone.findPointsByVoisins(5, 5)
    zone.draw()
    affichage(myMesh, zone)


main()
