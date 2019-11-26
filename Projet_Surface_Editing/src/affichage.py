import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from mesh import Mesh
from test_affichage import *
from itertools import *
from intrestZone import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def object(myMesh, face, color):
    glBegin(GL_LINES)
    face2 = face + (face[0],)
    for vertex in face2:
        glColor3f(color[0], color[1], color[2]);
        glVertex3fv(myMesh.points[vertex])
    glEnd()


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def affichage(myMesh):
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #Cube()
        color_red = (1.0, 0.0, 0.0)
        color_blue = (0.0, 0.0, 1.0)
        #color_green = (0.0, 1.0, 0.0)
        zone = IntrestZone(myMesh)
        zone.findPointsBydistance(myMesh.points[50], 1.5)
        for face in myMesh.facesIndexs:
            object(myMesh,face, color_blue)
        for face in zone.faces:
            object(myMesh,face, color_red)
        pygame.display.flip()
        pygame.time.wait(10)
