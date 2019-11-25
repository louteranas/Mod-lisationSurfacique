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
                    self.numberOfPoints = ligneData[0]
                    self.numberOfFaces = ligneData[1]
                    firstLigne = False
                    continue
                ligneData = ([f for f in ligne.split(" ")])
                if(len(ligneData)==3):
                    self.points.append(ligneData)
                if(len(ligneData)==4):
                    self.facesIndexs.append((ligneData[1], ligneData[2], ligneData[3]))

    def draw(self):
        ## TODO
