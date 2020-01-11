#!/usr/bin/env python3
import numpy as np
class Mesh:
    def __init__(self):
        self.numberOfPoints = 0
        self.numberOfFaces = 0
        self.points = [] #liste des tuples de points du mesh
        self.facesIndexs = []
        self.adjacentMatrix = []
        self.degreeMatrix = []


    def parseEntry(self, argFile = "../models/cylindre.off"):
        "parse et creer nos variables "
        with open(argFile, 'r') as argument:
            data = argument.read()
            lignes = data.split("\n")
            firstLigne = True
            for ligne in lignes:
                if(ligne == 'OFF'):
                    continue
                if(firstLigne):
                    ligneData = ([f for f in ligne.split(" ")])
                    self.numberOfPoints = int(ligneData[0])
                    self.numberOfFaces = int(ligneData[1])
                    firstLigne = False
                    continue
                ligneData = ([f for f in ligne.split(" ")])
                if("" in ligneData):
                    ligneData.remove("")
                if(len(ligneData) == 3):
                    self.points.append((float(ligneData[0]), float(ligneData[1]), float(ligneData[2])))
                if(len(ligneData) == 4):
                    self.facesIndexs.append((int(ligneData[1]), int(ligneData[2]), int(ligneData[3])))
            self.adjacentMatrix = np.asarray([np.asarray([0 for _ in range(self.numberOfPoints)]) for _ in range(self.numberOfPoints)])
        self.computeAdjacentMatrix()
        self.degreeMatrix = self.computeVerticesDegreeMatrix()


    def saveMeshOff(self):
        "enregitre le mesh obtenue dans un .off"
        print('mesh enregistré dans ../models/result_test.off')
        f = open('../models/result_test.off', 'w')
        f.write('OFF')
        f.write('\n')
        f.write(str(self.numberOfPoints))
        f.write(' ')
        f.write(str(self.numberOfFaces))
        f.write(' ')
        f.write('0') #nb of edge can be ignore
        f.write('\n')
        for point in self.points:
            f.write(str(point[0]))
            f.write(' ')
            f.write(str(point[1]))
            f.write(' ')
            f.write(str(point[2]))
            f.write('\n')
        for face in self.facesIndexs:
            f.write('3 ')
            f.write(str(face[0]))
            f.write(' ')
            f.write(str(face[1]))
            f.write(' ')
            f.write(str(face[2]))
            f.write('\n')
        f.close()


#Calcul des matrices A, D et L

    def computeAdjacentMatrix(self):
        "creer la matrice d'adjacence pour le mesh entier"
        for faceIndexs in self.facesIndexs:
            self.adjacentMatrix[faceIndexs[0]][faceIndexs[1]] = 1
            self.adjacentMatrix[faceIndexs[1]][faceIndexs[0]] = 1
            self.adjacentMatrix[faceIndexs[1]][faceIndexs[2]] = 1
            self.adjacentMatrix[faceIndexs[2]][faceIndexs[1]] = 1
            self.adjacentMatrix[faceIndexs[2]][faceIndexs[0]] = 1
            self.adjacentMatrix[faceIndexs[0]][faceIndexs[2]] = 1

    def verticesDegree(self):
        "retourne la diagonale de la matrice D"
        return [sum(self.adjacentMatrix[i]) for i in range(self.numberOfPoints)]

    def computeVerticesDegreeMatrix(self):
        "renvoie la matrice D"
        verticesDegree = self.verticesDegree()
        verticesDegreeMatrix = np.asarray([np.asarray([0 for _ in range(self.numberOfPoints)]) for _ in range(self.numberOfPoints)])
        for i in range(self.numberOfPoints):
            verticesDegreeMatrix[i][i] = verticesDegree[i]
        return verticesDegreeMatrix

    def computeLaplacianMatrix(self):
        "renvoie la matrice L"
        return np.identity(self.numberOfPoints) - np.dot(np.linalg.inv(self.computeVerticesDegreeMatrix()), self.adjacentMatrix)


#fonctions de recherche de voisins, récupération de points ...

    def getFirstVoisins(self, index):
        "renvoie la liste des voisins du point d'index index (sans le point lui meme)"
        voisins = []
        for i in range(self.numberOfPoints):
            if(self.adjacentMatrix[index][i] == 1):
                voisins.append(i)
        return voisins

    def getCoordonneesListePoints(self, listeIndexPoints):
        "renvoie les coordonnees d'une liste de points (dans une liste)"
        return [self.points[i] for i in listeIndexPoints]


    def getDegreeVoisins(self, index, degree):
        "renvoie la liste des voisins à une distance degree du point d'indice index"
        if(degree == 0):
            return []
        firstVoisins = self.getFirstVoisins(index)
        voisins = [firstVoisins]
        for _ in range(degree-1):
            degreeVoisins = []
            for voisin in voisins[-1]:
                degreeVoisins.extend(self.getFirstVoisins(voisin))
            degreeVoisins = list(set(degreeVoisins))
            voisins.append(degreeVoisins)
        return voisins

    def getAllVoisins(self, index, degree):
        "renvoie le voisinage du point d'indice index, degree étant la distance maximal des voisins"
        degreeVoisins = self.getDegreeVoisins(index, degree)
        allVoisins = []
        for voisins in degreeVoisins:
            for voisin in voisins:
                allVoisins.append(voisin)
        allVoisins = list(set(allVoisins))
        #on met le point en question à la fin
        if (index in allVoisins):
            allVoisins.remove(index)
        allVoisins.append(index)
        return allVoisins


#Pour la création du Handle

    def createHandle(self,listePointsHandle, newPointPos):
        "renvoie des nouvelles coordonnées automatique pour le Handle"
        newListePointsHandle = []
        for point in listePointsHandle:
            newListePointsHandle.append(tuple(map(lambda i, j: i*0.9 + j*0.1, newPointPos, point)))
        return newListePointsHandle


#pour l'affichage

    def arrayPoints(self):
        array = []
        for point in self.points:
            for coord in point:
                array.append(coord)
        return tuple(array)

    def arrayFaces(self):
        array = []
        for face in self.facesIndexs:
            for index in face:
                array.append(index)
        return array
