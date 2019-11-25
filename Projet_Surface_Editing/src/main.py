#!/usr/bin/env python3

from mesh import Mesh
import sys



def main():
    myMesh = Mesh()
    myMesh.parseEntry(sys.argv[1])
    myMesh.draw()

main()