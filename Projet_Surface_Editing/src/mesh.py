#!/usr/bin/env python3

class Mesh:
    def __init__(self):
        self.numberOfPoints = 0
        self.numberOfFaces = 0
        self.points = []
        self.facesIndexs = []
        self.adjacentMatrix = []


    def parseEntry(self, argFile):
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
                if(len(ligneData)==3):
                    self.points.append((float(ligneData[0]), float(ligneData[1]), float(ligneData[2])))
                if(len(ligneData)==4):
                    self.facesIndexs.append((int(ligneData[1]), int(ligneData[2]), int(ligneData[3])))
            self.adjacentMatrix = [[0 for _ in range(self.numberOfPoints)] for _ in range(self.numberOfPoints)]
        self.computeAdjacentMatrix()

    def computeAdjacentMatrix(self):
        for faceIndexs in self.facesIndexs:
            self.adjacentMatrix[faceIndexs[0]][faceIndexs[1]] = 1
            self.adjacentMatrix[faceIndexs[1]][faceIndexs[0]] = 1
            self.adjacentMatrix[faceIndexs[1]][faceIndexs[2]] = 1
            self.adjacentMatrix[faceIndexs[2]][faceIndexs[1]] = 1
            self.adjacentMatrix[faceIndexs[2]][faceIndexs[0]] = 1
            self.adjacentMatrix[faceIndexs[0]][faceIndexs[2]] = 1   
    
    def getFirstVoisins(self, index):
        voisins = []
        print(index)
        for i in range(self.numberOfPoints):
            if(self.adjacentMatrix[index][i] == 1):
                voisins.append(i)
        return voisins

    def getDegreeVoisins(self, index, degree):
        # if(degree == 1):
        #     print("coucou")
        #     return self.getFirstVoisins(index)
        # voisins = self.getFirstVoisins(index)
        # for voisin in voisins:
        #     return voisins.extend(self.getVoisins(voisin, degree-1))
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
        degreeVoisins = self.getDegreeVoisins(index, degree)
        allVoisins = []
        for voisins in degreeVoisins:
            for voisin in voisins:
                allVoisins.append(voisin)
        allVoisins = list(set(allVoisins))
        return allVoisins



    def draw(self):
        for face in self.facesIndexs:
            print('face: ')
            for vertex in face:
                print(vertex)
