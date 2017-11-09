# point cloud
__author__ = 'JACK'
from pymel.core import *
import random
point_cloud = []


def gen(n, center, radius, level):
    if level is 0:
        return

    global point_cloud
    for i in range(n):
        p = dt.Vector(random.uniform(-1,1),
                     random.uniform(-1,1),
                    random.uniform(-1,1)) * radius + center
        point_cloud.append(p)
        gen(n,p,radius*0.5,level-1)

gen(3, dt.Point(0,0,0), 1.0, 3)
emit(object=particle()[0], position=point_cloud)