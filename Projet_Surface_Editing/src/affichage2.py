#! /usr/bin/env python3

import pyglet
from mesh import Mesh
from pyglet.gl import *
import math
import sys
from intrestZone import IntrestZone
import copy 

from minimization import *
from minimization2 import *

###### Mesh definitin
originalMesh = Mesh()
originalMesh.parseEntry(sys.argv[1]) if len(sys.argv) > 1 else originalMesh.parseEntry()
myMesh = copy.deepcopy(originalMesh)

##### Handle point index
originIndex = 400



##### Interest Zone
originalZone = IntrestZone(originalMesh)
zone = IntrestZone(myMesh)
tailleHandle = 0 
zoneSize = 0
handleZone = IntrestZone(myMesh)
handleZone.findPointsByVoisins(originIndex, tailleHandle)
zone.findPointsByVoisins(originIndex, zoneSize)
modified = False
        
def modifyMesh(myMesh, coordx, coordy):
    global modified
    global zone
    global tailleHandle
    global handleZone
    listPoints = []
    if(tailleHandle == 0):
        sauvPoint = myMesh.points[originIndex]
        newPointPos = (myMesh.points[originIndex][0]+coordx, myMesh.points[originIndex][1]+ coordy, myMesh.points[originIndex][2])
        listPoints.append(newPointPos)
    elif(tailleHandle > 0):
        newPointPos = (myMesh.points[originIndex][0]+coordx, myMesh.points[originIndex][1]+ coordy, myMesh.points[originIndex][2])
        listePointsHandle = handleZone.intrestPoints
        sauvListePointsHandle = myMesh.getCoordonneesListePoints(listePointsHandle)
        listPoints = myMesh.createHandle(sauvListePointsHandle, newPointPos)
    res = minimizationHandle(myMesh, zone, originIndex, listPoints)
    for i in range(zone.numberOfPoints):
         myMesh.points[zone.intrestPoints[i]] = (res[0][i], res[1][i], res[2][i])
    modified = True
    return IntrestZone

def showInterestZone():
    global zone
    global zoneSize
    global handleZone
    global tailleHandle
    zone.findPointsByVoisins(originIndex, zoneSize)
    points = zone.getPositions()
    handlePoints = handleZone.getPositions()
    pyglet.graphics.draw_indexed(int(len(points)/3), pyglet.gl.GL_TRIANGLES, zone.getFaces(), ('v3f', points), ('c3B', tuple([255,0,0]*int(len(points)/3))))
    pyglet.graphics.draw_indexed(int(len(handlePoints)/3), pyglet.gl.GL_TRIANGLES, handleZone.getFaces(), ('v3f', handlePoints), ('c3B', tuple([0,255,0]*int(len(handlePoints)/3))))


cubeWindow = pyglet.window.Window(width = 1200, height = 1200)
@cubeWindow.event
def on_show():
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
    # Set up projection matrix.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(45.0, float(cubeWindow.width)/cubeWindow.height, 0.1, 360)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glTranslatef(0, 0, -6)
    pyglet.gl.glColor4f(1.0,1.,1.0,0.2)
    pyglet.graphics.draw_indexed(len(myMesh.points), pyglet.gl.GL_TRIANGLES, myMesh.arrayFaces(), ('v3f', myMesh.arrayPoints()))

@cubeWindow.event
def on_draw():
    global modified
    global zone
    global tailleHandle
    pyglet.graphics.draw_indexed(len(myMesh.points), pyglet.gl.GL_TRIANGLES, myMesh.arrayFaces(), ('v3f', myMesh.arrayPoints()), ('c3B', tuple([255,255,255]*len(myMesh.points))))
    if(zoneSize > 0 or tailleHandle > 0):
        showInterestZone()
        
   


@cubeWindow.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    cubeWindow.clear()
    if scroll_y > 0:
        pyglet.gl.glTranslatef( 0, 0, 0.9)#0.05)
    if scroll_y < 0:
        pyglet.gl.glTranslatef( 0, 0, -0.9)#-0.05)

@cubeWindow.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    cubeWindow.clear()
    if(button == pyglet.window.mouse.RIGHT):
        if dx > 0:
            pyglet.gl.glTranslatef( 0.01, 0, 0)
        elif dx < 0:
            pyglet.gl.glTranslatef( -0.01, 0, 0.)
        elif dy > 0:
            pyglet.gl.glTranslatef( 0, 0.01, 0)
        elif dy < 0:
            pyglet.gl.glTranslatef( 0, -0.01, 0)

    if(button == pyglet.window.mouse.LEFT):
        if dx > 0:
            pyglet.gl.glRotatef(3*dx/4, 1, 0, 0)
        elif dx < 0:
            pyglet.gl.glRotatef(-3*dx/4, 1, 0, 0)
        elif dy > 0:
            pyglet.gl.glRotatef(3*dy/4, 0, 1, 0)
        elif dy < 0:
            pyglet.gl.glRotatef(-3*dy/4, 0, 1, 0)

    if(button == pyglet.window.mouse.MIDDLE):
        if dy > 0:
            pyglet.gl.glRotatef(3*dy/4, 0, 0, 1)
        elif dy < 0:
            pyglet.gl.glRotatef(-3*dy/4, 0, 0, 1)

def mouse_to_3d(x, y, z = 1.0, local_transform = False):
    x = float(x)
    y = float(y)
    pmat = (GLdouble * 16)()
    mvmat = (GLdouble * 16)()
    viewport = (GLint * 4)()
    px = (GLdouble)()
    py = (GLdouble)()
    pz = (GLdouble)()
    glGetIntegerv(GL_VIEWPORT, viewport)
    glGetDoublev(GL_PROJECTION_MATRIX, pmat)
    glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)
    gluUnProject(x, y, z, mvmat, pmat, viewport, px, py, pz)
    return (px.value, py.value, pz.value)


@cubeWindow.event
def on_mouse_press(x, y, button, modifiers):
    cubeWindow.clear()
    a = (GLuint * 1)(0)
    glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_UNSIGNED_INT, a)
    if(modifiers == pyglet.window.key.MOD_CTRL):
        sphere = gluNewQuadric()
        gluSphere(sphere,0.01,10,10)
        worldCoords= mouse_to_3d(x, y)
        modifyMesh(myMesh, worldCoords[0]/50, worldCoords[1]/50)


@cubeWindow.event
def on_key_press(symbol, modifiers):
    global zone
    global handleZone
    global zoneSize
    global originalZone
    global myMesh
    global originalMesh
    global originIndex
    global tailleHandle
    cubeWindow.clear()
    if(symbol == pyglet.window.key.A):
        pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    if(symbol == pyglet.window.key.Q):
        pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    if(symbol == pyglet.window.key.UP):
        zoneSize += 1

    if(symbol == pyglet.window.key.DOWN):
        if(zoneSize>tailleHandle):
            zoneSize -= 1
        else:
            print("can't have an ROI smaller than the handle size")

    if(symbol == pyglet.window.key.I):
        tailleHandle += 1
        if(tailleHandle > zoneSize):
            zoneSize += 1
        handleZone.reset()
        handleZone.findPointsByVoisins(originIndex, tailleHandle)

    if(symbol == pyglet.window.key.K):
        tailleHandle -= 1
        handleZone.reset()
        handleZone.findPointsByVoisins(originIndex, tailleHandle)
    
    if(symbol == pyglet.window.key.RIGHT):
        originIndex += 1    
        handleZone.reset()
        handleZone.findPointsByVoisins(originIndex, tailleHandle)
        zone.reset()
        zone.findPointsByVoisins(originIndex, zoneSize)

    if(symbol == pyglet.window.key.LEFT):
        originIndex -= 1
        handleZone.reset()
        handleZone.findPointsByVoisins(originIndex, tailleHandle)
        zone.reset()
        zone.findPointsByVoisins(originIndex, zoneSize)

    if(symbol == pyglet.window.key.N):
        originIndex += 100
        originIndex = originIndex%myMesh.numberOfPoints
        handleZone.reset()
        handleZone.findPointsByVoisins(originIndex, tailleHandle)
        zone.reset()
        zone.findPointsByVoisins(originIndex, zoneSize)

    if(symbol == pyglet.window.key.B):
        originIndex -= 100
        originIndex = originIndex%myMesh.numberOfPoints
        handleZone.reset()
        handleZone.findPointsByVoisins(originIndex, tailleHandle)
        zone.reset()
        zone.findPointsByVoisins(originIndex, zoneSize)
    




pyglet.app.run()
