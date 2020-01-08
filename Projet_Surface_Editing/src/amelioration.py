from mesh import Mesh
from intrestZone import IntrestZone
import sys
from affichage import *
import numpy as np
from numpy.linalg import inv

import scipy

def newB(monMesh, maZone, originPointIndex, nouveauPoint, bx, by, bz):
    newbx = []
    newby = []
    newbz = []
    for i, point in enumerate(maZone.intrestPoints):#pour tout i

        Ai = []
        bi = []
        #print("point ", point)
        #print(len([e for e in monMesh.getFirstVoisins(point)]), "voisins", [e for e in monMesh.getFirstVoisins(point)])
        if point== originPointIndex:
            bi.append(nouveauPoint[0])
            bi.append(nouveauPoint[1])
            bi.append(nouveauPoint[2])
        else:
            bi.append(monMesh.points[point][0])
            bi.append(monMesh.points[point][1])
            bi.append(monMesh.points[point][2])
        Ai.append([monMesh.points[point][0], 0, monMesh.points[point][2], -monMesh.points[point][1], 1, 0, 0])
        Ai.append([monMesh.points[point][1], -monMesh.points[point][2], 0, monMesh.points[point][0], 0, 1, 0])
        Ai.append([monMesh.points[point][2], monMesh.points[point][1], -monMesh.points[point][0], 0, 0, 1, 0])
        for voisin in monMesh.getFirstVoisins(point):
            if point== originPointIndex:
                bi.append(nouveauPoint[0])
                bi.append(nouveauPoint[1])
                bi.append(nouveauPoint[2])
            else:
                bi.append(monMesh.points[voisin][0])
                bi.append(monMesh.points[voisin][1])
                bi.append(monMesh.points[voisin][2])
            Ai.append([monMesh.points[voisin][0], 0, monMesh.points[voisin][2], -monMesh.points[voisin][1], 1, 0, 0])
            Ai.append([monMesh.points[voisin][1], -monMesh.points[voisin][2], 0, monMesh.points[voisin][0], 0, 1, 0])
            Ai.append([monMesh.points[voisin][2], monMesh.points[voisin][1], -monMesh.points[voisin][0], 0, 0, 1, 0])
        Ai = np.array(Ai)
        bi = np.array(bi)
        #print("Ai ", Ai)
        #print("taille Ai", len(Ai), len(Ai[0]))

        AiTAi = ((Ai.transpose()).dot(Ai))
        #print("AiTAi", AiTAi, len(AiTAi))
        #print("taille bi", len(bi), bi)
        #resolution de l'équation: (AiTAi) sihiiT = AiTbi
        sihitiT = np.linalg.lstsq(AiTAi, (Ai.transpose()).dot(bi))#possibilité de plusieurs solution je prend la premiere par default
        s = sihitiT[0][0]
        h = [sihitiT[0][1], sihitiT[0][2], sihitiT[0][3]]
        t = [sihitiT[0][4], sihitiT[0][5], sihitiT[0][6]]
        Ti =np.array([
        [s, -h[2], h[1], t[0]],
        [h[2], s, -h[0], t[1]],
        [-h[1], h[0], s, t[2]]
        ])
        newb = Ti.dot(np.array([bx[i], by[i], bz[i], 1]).transpose())
        #print("newb: ", newb)
        #remet sous forme classique
        #newb = [newb[0]/newb[3], newb[1]/newb[3], newb[2]/newb[3] ]
        #print("sihitiT: ", sihitiT[0], "taille", len(sihitiT[0]))
        newbx.append(newb[0])
        newby.append(newb[1])
        newbz.append(newb[2])
    return newbx, newby, newbz
