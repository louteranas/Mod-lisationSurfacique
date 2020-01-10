#! /usr/bin/env python3

import pyglet
from mesh import Mesh
from pyglet.gl import *
import math
import sys
from intrestZone import IntrestZone

from minimization import *
from minimization2 import *

myMesh = Mesh()
myMesh.parseEntry(sys.argv[1]) if len(sys.argv) > 1 else myMesh.parseEntry()
# self.points = pyglet.graphics.vertex_list(4, ('v3f/stream', createpolygons(4, -self.width/2, -self.height/2)), ('c3B', colordata(4)))
        
        
def main(myMesh):
    originIndex = 400
    sauvPoint = myMesh.points[originIndex]
    newPointPos = (myMesh.points[originIndex][0]+0.5, myMesh.points[originIndex][1]+1, myMesh.points[originIndex][2])
    zone = IntrestZone(myMesh)
    zone.findPointsByVoisins(originIndex,2)
    res = minimization2(myMesh, zone, originIndex, newPointPos)
    for i in range(zone.numberOfPoints):
         myMesh.points[zone.intrestPoints[i]] = (res[0][i], res[1][i], res[2][i])



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

@cubeWindow.event
def on_draw():
    cubeWindow.clear()
    mesh = pyglet.graphics.draw_indexed(len(myMesh.points), pyglet.gl.GL_TRIANGLES, myMesh.arrayFaces(), ('v3f', myMesh.arrayPoints()))

@cubeWindow.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y > 0:
        pyglet.gl.glTranslatef( 0, 0, 0.05)
        # pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    if scroll_y < 0:
        pyglet.gl.glTranslatef( 0, 0, -0.05)
        # pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

@cubeWindow.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
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
            pyglet.gl.glRotatef(0.5, 1, 0, 0)
        elif dx < 0:
            pyglet.gl.glRotatef(-0.5, 1, 0, 0)
        elif dy > 0:
            pyglet.gl.glRotatef(0.5, 0, 1, 0)
        elif dy < 0:
            pyglet.gl.glRotatef(-0.5, 0, 1, 0)
    if(button == pyglet.window.mouse.MIDDLE):
        if dy > 0:
            pyglet.gl.glRotatef(0.5, 0, 0, 1)
        elif dy < 0:
            pyglet.gl.glRotatef(-0.5, 0, 0, 1)

@cubeWindow.event
def on_key_press(symbol, modifiers):
    if(symbol == pyglet.window.key.A):
        pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    if(symbol == pyglet.window.key.Q):
        pyglet.gl.glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    if(symbol == pyglet.window.key.Z):
        main(myMesh)




pyglet.app.run()
