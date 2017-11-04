#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : back to ground
# description : ''
# author      : MengWei
# date        : 
# version     :
# usage       :
# notes       :


obj = selected()[0]
ground = selected()[1]
def getLowestVtx(obj):
    vtx = [(v.currentItemIndex(), v.getPosition('world')) for v in obj.vtx]
    vtx.sort(key=lambda a:a[1][1])
    return vtx[0]
p = getLowestVtx(obj)[1]
intersected, intersection, faceids = ground.intersect(p, (0,-1,0), space='world')

def facePos(self):
    return sum(self.getPoints('world'))/len(self.getPoints('world'))
from types import MethodType
MeshFace.facePos = MethodType(facePos, None, MeshFace)

node = ground.node()
F = node.f[faceids[0]]
face_p = F.facePos()

dis_y = face_p - p
# spaceLocator(p=face_p)

select(obj)
move(0,dis_y.y,0,r=1)
