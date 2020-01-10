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
zone = IntrestZone(myMesh)
zoneSize = 0
zone.findPointsByVoisins(originIndex, zoneSize)
modified = False
        
def modifyMesh(myMesh, coordx, coordy):
    global modified
    global zone
    sauvPoint = myMesh.points[originIndex]
    #newPointPos = (myMesh.points[originIndex][0]+0.5, myMesh.points[originIndex][1]+1, myMesh.points[originIndex][2])
    newPointPos = (coordx, coordy, myMesh.points[originIndex][2])
    res = minimization2(myMesh, zone, originIndex, newPointPos)
    for i in range(zone.numberOfPoints):
         myMesh.points[zone.intrestPoints[i]] = (res[0][i], res[1][i], res[2][i])
    modified = True
    return IntrestZone

def showInterestZone():
    global zone
    global zoneSize
    zone.findPointsByVoisins(originIndex, zoneSize)
    points = zone.getPositions()
    pyglet.graphics.draw_indexed(int(len(points)/3), pyglet.gl.GL_TRIANGLES, zone.getFaces(), ('v3f', points), ('c3B', tuple([255,0,0]*int(len(points)/3))))


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
    mesh = pyglet.graphics.draw_indexed(len(myMesh.points), pyglet.gl.GL_TRIANGLES, myMesh.arrayFaces(), ('v3f', myMesh.arrayPoints()))

@cubeWindow.event
def on_draw():
    global modified
    global zone
    mesh = pyglet.graphics.draw_indexed(len(myMesh.points), pyglet.gl.GL_TRIANGLES, myMesh.arrayFaces(), ('v3f', myMesh.arrayPoints()), ('c3B', tuple([255,255,255]*len(myMesh.points))))
    if(zoneSize > 0):
        showInterestZone()
        
   


@cubeWindow.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    cubeWindow.clear()
    if scroll_y > 0:
        pyglet.gl.glTranslatef( 0, 0, 0.9)#0.05)
        # pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    if scroll_y < 0:
        pyglet.gl.glTranslatef( 0, 0, -0.9)#-0.05)
        # pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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
    y = 1200 - float(y)
    # The following could work if we were not initially scaling to zoom on
    # the bed
    # if self.orthographic:
    #    return (x - self.width / 2, y - self.height / 2, 0)
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
    print("x value = "+ str(x)+ " | y value = " +str(y))
    a = (GLuint * 1)(0)
    glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_UNSIGNED_INT, a)
    print(a[0])
    if(modifiers == pyglet.window.key.MOD_CTRL):
        sphere = gluNewQuadric()
        gluSphere(sphere,0.01,10,10)
        worldCoords= mouse_to_3d(x/1200, y/1200)
        modifyMesh(myMesh, worldCoords[0]/60, worldCoords[1]/60)


@cubeWindow.event
def on_key_press(symbol, modifiers):
    global zoneSize
    global myMesh
    global originalMesh
    cubeWindow.clear()
    if(symbol == pyglet.window.key.A):
        pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    if(symbol == pyglet.window.key.Q):
        pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    if(symbol == pyglet.window.key.UP):
        zoneSize += 1
    if(symbol == pyglet.window.key.DOWN):
        zoneSize -= 1
    if(symbol == pyglet.window.key.R):
        myMesh = copy.deepcopy(originalMesh)
        zone = IntrestZone(myMesh)
        zoneSize = 0
        zone.findPointsByVoisins(originIndex, zoneSize)
    # if(symbol == pyglet.window.key.Z):
    #     return




pyglet.app.run()
