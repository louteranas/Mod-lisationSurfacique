#!/usr/bin/env python3

from mesh import Mesh
from intrestZone import IntrestZone
import sys
from affichage import *

from minimization import *
from minimization2 import *

import os



def main():
    #creation de notre class mesh
    myMesh = Mesh()

    #parsage du .off placé en argument
    myMesh.parseEntry(sys.argv[1]) if len(sys.argv) > 1 else myMesh.parseEntry()
    baseMeshPath = sys.argv[1] if len(sys.argv) > 1 else "../models/cylindre.off"

    #choix du point centrale du Handle
    originIndex = 400
    sauvPoint = myMesh.points[originIndex]
    newPointPos = (myMesh.points[originIndex][0]+0.5, myMesh.points[originIndex][1]+1, myMesh.points[originIndex][2])

    #creation du Handle
    tailleHandle = 2
    listePointsHandle = myMesh.getAllVoisins(originIndex, tailleHandle)
    sauvListePointsHandle = myMesh.getCoordonneesListePoints(listePointsHandle)
    newListePointsHandle = myMesh.createHandle(sauvListePointsHandle, newPointPos)

    #print("point d'origine", sauvPoint, "newPointPos", newPointPos)

    #Creation de la ROI
    tailleROI= 5
    zone = IntrestZone(myMesh)
    zone.findPointsByVoisins(originIndex,tailleROI)

    #lancement de la minimisation
    res = minimization2(myMesh, zone, originIndex, newPointPos, False)
    for i in range(zone.numberOfPoints):
         myMesh.points[zone.intrestPoints[i]] = (res[0][i], res[1][i], res[2][i])
    myMesh.saveMeshOff()

    #print("\n point d'origine: ", sauvPoint)
    #print("\n point voulu: ", newPointPos)
    #print("\n point obtenu: ", myMesh.points[originIndex])
    affichage(myMesh, zone,  originIndex, newPointPos, sauvPoint)




main()
