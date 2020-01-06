# import pygame
# from pygame.locals import *
# import numpy as np
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from mesh import Mesh
#
# from itertools import *
# from intrestZone import *
#
#
# #-------------------------Exemple pour un cube-----------------------------------------
# verticies = (
#     (1, -1, -1),
#     (1, 1, -1),
#     (-1, 1, -1),
#     (-1, -1, -1),
#     (1, -1, 1),
#     (1, 1, 1),
#     (-1, -1, 1),
#     (-1, 1, 1)
#     )
#
# edges = (
#     (0,1),
#     (0,3),
#     (0,4),
#     (2,1),
#     (2,3),
#     (2,7),
#     (6,3),
#     (6,4),
#     (6,7),
#     (5,1),
#     (5,4),
#     (5,7)
#     )
#
#
#
# def Cube():
#     glBegin(GL_LINES)
#     for edge in edges:
#         for vertex in edge:
#             glVertex3fv(verticies[vertex])
#     glEnd()
# #--------------------Fin d'exemple pour le cube----------------------------------------------------
#
#
#
# #genere dans openGL un les edges de la face(liste de trois numero de vertex) du mesh en question avec la couleur choisie
# def object(myMesh, face, color):
#     glBegin(GL_LINES)
#     face2 = face + (face[0],)
#     for vertex in face2:
#         glColor3f(color[0], color[1], color[2]);
#         glVertex3fv(myMesh.points[vertex])
#     glEnd()
#
#
#
#
#
# def IdentityMat44():
#     return np.matrix(np.identity(4), copy=False, dtype='float32')
#
# def affichage(myMesh, zone):
#     pygame.init()
#     display = (1600,1000)
#     pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
#     tx = 0
#     ty = 0
#     tz = 0
#     rx = 0
#     ry = 0
#     rz = 0
#
#     glMatrixMode(GL_PROJECTION)
#     gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
#
#     view_mat = IdentityMat44()
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     glTranslatef(0, 0, -10)
#     glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
#     glLoadIdentity()
#
#     while True:
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()
#                     quit()
#                 if   event.key == pygame.K_RIGHT:     tx =  0.1
#                 elif event.key == pygame.K_LEFT:     tx = -0.1
#                 elif event.key == pygame.K_UP:     ty =  0.1
#                 elif event.key == pygame.K_DOWN:     ty = -0.1
#                 elif event.key == pygame.K_EQUALS:     tz =  0.1
#                 elif event.key == pygame.K_MINUS:     tz = -0.1
#                 elif event.key == pygame.K_a: rz =  1.0
#                 elif event.key == pygame.K_z:  rz = -1.0
#                 elif event.key == pygame.K_s:    rx =  1.0
#                 elif event.key == pygame.K_d:  rx = -1.0
#                 elif event.key == pygame.K_x:    ry =  1.0
#                 elif event.key == pygame.K_w:  ry = -1.0
#             elif event.type == pygame.KEYUP:
#                 if   event.key == pygame.K_RIGHT     and tx > 0: tx = 0
#                 elif event.key == pygame.K_LEFT     and tx < 0: tx = 0
#                 elif event.key == pygame.K_UP     and ty > 0: ty = 0
#                 elif event.key == pygame.K_DOWN     and ty < 0: ty = 0
#                 elif event.key == pygame.K_EQUALS     and tz > 0: tz = 0
#                 elif event.key == pygame.K_MINUS     and tz < 0: tz = 0
#                 elif event.key == pygame.K_a and rz > 0: rz = 0.0
#                 elif event.key == pygame.K_z  and rz < 0: rz = 0.0
#                 elif event.key == pygame.K_s and rx > 0: rx = 0.0
#                 elif event.key == pygame.K_d  and rx < 0: rx = 0.0
#                 elif event.key == pygame.K_x and ry > 0: ry = 0.0
#                 elif event.key == pygame.K_w  and ry < 0: ry = 0.0
#
#
#         glPushMatrix()
#         glLoadIdentity()
#         glTranslatef(tx,ty,tz)
#         if (rz!= 0):
#             glTranslatef(myMesh.points[0][0],myMesh.points[0][1],myMesh.points[0][2])
#             glRotatef(rz*10, 0, 0, 1)
#             glTranslatef(-myMesh.points[0][0],-myMesh.points[0][1],-myMesh.points[0][2])
#         elif (rx!= 0):
#             glTranslatef(0, 0, -10)
#             glRotatef(rx*10, 1, 0, -10)
#             glTranslatef(0, 0, 10)
#         elif (ry!= 0):
#
#             glRotatef(ry*10, 0, 1, 0)
#
#         #glRotatef(ry, 1, 0, 0)
#         glMultMatrixf(view_mat)
#
#         glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
#
#         glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#         color_white = (1.0, 1.0, 1.0)
#         color_red = (1.0, 0.0, 0.0)
#         color_blue = (0.0, 0.0, 1.0)
#         color_green = (0.0, 1.0, 0.0)
#
#         # for face in myMesh.facesIndexs:
#         #    object(myMesh,face, color_white)
#         for face in myMesh.facesIndexs:
#             object(myMesh,face, color_white)
#         for face in zone.faces:
#             object(myMesh,face, color_red)
#         glPopMatrix()
#
#
#
#
#         pygame.display.flip()
#         pygame.time.wait(10)
#
#
#
#
#     #
#     # pygame.init()
#     # display = (800,600)
#     # pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
#     #
#     # gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
#     #
#     # glTranslatef(0.0,0.0, -5)
#     #
#     # while True:
#     #     for event in pygame.event.get():
#     #         if event.type == pygame.QUIT:
#     #             pygame.quit()
#     #             quit()
#     #
#     #     #glRotatef(1, 3, 1, 1)
#     #     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#     #     #Cube()  #exemple simple d'un cube
#     #     color_red = (1.0, 0.0, 0.0)
#     #     color_white = (1.0, 1.0, 1.0)
#     #     color_blue = (0.0, 0.0, 1.0)
#     #     color_green = (0.0, 1.0, 0.0)
#     #     zone = IntrestZone(myMesh)
#     #     zone.findPointsBydistance(myMesh.points[50], 0.5)
#     #     for face in myMesh.facesIndexs:
#     #         object(myMesh,face, color_white)
#     #     for face in zone.faces:
#     #         object(myMesh,face, color_red)
#     #     pygame.display.flip()
#     #     pygame.time.wait(10)
