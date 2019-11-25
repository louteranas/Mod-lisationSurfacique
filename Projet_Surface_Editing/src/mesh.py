#!/usr/bin/env python3

class Mesh:
    def __init__(self):
        self.numberOfPoints = 0
        self.numberOfFaces = 0
        self.points = []
        self.facesIndexs = []


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

    def draw(self):
        for face in self.facesIndexs:
            print('face: ')
            for vertex in face:
                print(vertex)
