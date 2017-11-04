import pymel.core as pm
import maya.mel as mel
setObj=pm.ls( sl=True )
for a in setObj:
    if len( a.split(':') ):
        newName = a.split( ':' )[1]
        a.rename( newName )
mel.eval('print \"%s\"' % u'重名成功!')