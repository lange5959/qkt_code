# -*- coding: utf-8 -*-
# title       : Nucleus控制器
# description : ''
# author      :
# date        :
# version     :
# usage       :
# notes       :

import maya.cmds as cmds
import maya.mel as mel


class myUI():
    def __init__(self):
        self.winName = 'Nucleus控制器'
        self.UI()

    def UI(self):
        if cmds.window(self.winName, q=True, exists=True):
            cmds.deleteUI(self.winName, window=True)
        if cmds.windowPref(self.winName, exists=True):
            cmds.windowPref(self.winName, remove=True)
        cmds.window(self.winName, widthHeight=(415, 200), s=False, bgc=[0.2, 0.2, 0.2])
        self.form = cmds.formLayout()
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(self.form, edit=True, attachForm=(
        (self.tabs, 'top', 0), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)))

        self.child1 = cmds.formLayout(numberOfDivisions=700)
        lghtBtn = [0.45, 0.45, 0.45]
        medBtn = [0.25, 0.25, 0.25]
        darkBtn = [0.15, 0.15, 0.15]

        self.wb = cmds.symbolButton(image='posAir.png', c=self.createWCTRL, w=80, h=58, bgc=[0.22, 0.22, 0.2],
                                    ann="Create Wind CTRL")
        self.gb = cmds.symbolButton(image='posGravity.png', c=self.createGCTRL, w=80, h=58, bgc=[0.2, 0.22, 0.22],
                                    ann="Create Gravity CTRL")
        self.queryList = ['nRigid', 'nucleus', 'nCloth', 'dynamicConstraint']
        footerText1 = cmds.text(label='"点击"下方标志，生成风向或重力控制器，此控制器可以随意的移动缩放大小', )
        footerText2 = cmds.text(label='注意当"旋转"它的时候，Nucleus的风向或重力会随控制器的方向而改变', )

        cmds.formLayout(self.child1, edit=True, attachForm=[
        ],
                        attachPosition=[
                            (self.wb, 'left', 70, 0), (self.wb, 'top', 0, 300),
                            (self.gb, 'left', 260, 0), (self.gb, 'top', 0, 300),
                            (footerText2, 'top', 0, 70), (footerText2, 'left', 0, 3)])
        cmds.setParent('..')
        cmds.tabLayout(self.tabs, edit=True, tabLabel=((self.child1, '风向和重力')), bgc=[0.2, 0.2, 0.2])
        cmds.showWindow(self.winName)

    ## defining create nucleus wind/gravity control commands

    def createWCTRL(self, *args):
        if cmds.objExists('windCTRL'):
            cmds.error('请勿重复创建，此功能后续添加')
            cmds.select('windCtrl')
        else:
            cmds.curve(n='pvWindArrow', d=1,
                       p=[(0, 15, 0), (-3, 4, -3), (3, 4, -3), (0, 15, 0), (3, 4, 3), (-3, 4, 3), (0, 15, 0),
                          (3, 4, -3),
                          (1, 4, -1), (2, -15, -2), (-2, -15, -2), (-1, 4, -1), (-3, 4, -3), (-3, 4, 3), (-1, 4, 1),
                          (-2, -15, 2), (2, -15, 2),
                          (1, 4, 1), (3, 4, 3), (3, 4, -3), (1, 4, -1), (-1, 4, -1), (-1, 4, 1), (1, 4, 1), (1, 4, -1),
                          (1, 4, -1), (2, -15, -2),
                          (2, -15, 2), (-2, -15, 2), (-2, -15, -2)], k=range(30))
            cmds.rotate(0, 0, -90)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=True)
            getShape = cmds.listRelatives(s=True, pa=True)[0]
            cmds.rename(getShape, 'pvWindArrowShape')
            cmds.spaceLocator(n='pvWindOrigin')
            cmds.setAttr('pvWindOrigin.visibility', 0)
            cmds.spaceLocator(n='pvWindAim')
            cmds.setAttr('pvWindAim.visibility', 0)
            cmds.group('pvWindAim', n='pvWindAim_Null')
            cmds.setAttr('pvWindAim.translateX', 1)
            cmds.aimConstraint('pvWindAim', 'pvWindOrigin')
            cmds.group('pvWindArrow', n='windCTRL')
            cmds.parentConstraint('windCTRL', 'pvWindAim_Null')
            cmds.select('pvWindArrowShape', 'windCTRL')
            cmds.parent(r=True, s=True)
            cmds.delete('pvWindArrow')
            cmds.pointConstraint('windCTRL', 'pvWindOrigin')
            cmds.pickWalk(direction="up")
            cmds.addAttr(ln='dynamicAmplitude', nn='Dynamic  Amplitude', at='float', dv=1)
            cmds.connectAttr('windCTRL.dynamicAmplitude', 'pvWindAim.translateX')
            cmds.setAttr('windCTRL.dynamicAmplitude', k=True)
            cmds.setAttr('pvWindArrowShape.overrideEnabled', 1)
            cmds.setAttr('pvWindArrowShape.overrideColor', 22)
            cmds.group('pvWindOrigin', 'pvWindAim_Null', 'windCTRL', n='windCTRL_GRP')
            cmds.setAttr('windCTRL_GRP.translateX', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.translateY', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.translateZ', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.rotateX', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.rotateY', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.rotateZ', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.scaleX', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.scaleY', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.scaleZ', k=False, l=True)
            cmds.setAttr('windCTRL_GRP.visibility', k=False, l=True)
            for eachNucleus in cmds.ls(type='nucleus'):
                cmds.connectAttr('pvWindOrigin_aimConstraint1.constraintVectorX', '%s.windDirectionX' % eachNucleus)
                cmds.connectAttr('pvWindOrigin_aimConstraint1.constraintVectorY', '%s.windDirectionY' % eachNucleus)
                cmds.connectAttr('pvWindOrigin_aimConstraint1.constraintVectorZ', '%s.windDirectionZ' % eachNucleus)
            cmds.select('windCTRL');

    def createGCTRL(self, *args):
        if cmds.objExists('gravCTRL'):
            cmds.error('请勿重复创建')
            cmds.select('gravCTRL')
        else:
            cmds.curve(n='pvGravArrow', d=1,
                       p=[(0, 15, 0), (-4, 4, -4), (4, 4, -4), (0, 15, 0), (4, 4, 4), (-4, 4, 4), (0, 15, 0),
                          (4, 4, -4),
                          (2, 4, -2), (3, -15, -3), (-3, -15, -3), (-2, 4, -2), (-4, 4, -4), (-4, 4, 4), (-2, 4, 2),
                          (-3, -15, 3), (3, -15, 3),
                          (2, 4, 2), (4, 4, 4), (4, 4, -4), (2, 4, -2), (-2, 4, -2), (-2, 4, 2), (2, 4, 2), (2, 4, -2),
                          (2, 4, -2), (3, -15, -3),
                          (3, -15, 3), (-3, -15, 3), (-3, -15, -3)], k=range(30))
            cmds.rotate(180, 0, 0)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=True)
            getShape = cmds.listRelatives(s=True, pa=True)[0]
            cmds.rename(getShape, 'pvGravArrowShape')
            cmds.spaceLocator(n='pvGravOrigin')
            cmds.setAttr('pvGravOrigin.visibility', 0)
            cmds.spaceLocator(n='pvGravAim')
            cmds.setAttr('pvGravAim.visibility', 0)
            cmds.group('pvGravAim', n='pvGravAim_Null')
            cmds.setAttr('pvGravAim.translateY', -1)
            cmds.aimConstraint('pvGravAim', 'pvGravOrigin')
            cmds.group('pvGravArrow', n='gravCTRL')
            cmds.parentConstraint('gravCTRL', 'pvGravAim_Null')
            cmds.select('pvGravArrowShape', 'gravCTRL')
            cmds.parent(r=True, s=True)
            cmds.delete('pvGravArrow')
            cmds.pointConstraint('gravCTRL', 'pvGravOrigin')
            cmds.pickWalk(direction="up")
            cmds.addAttr(ln='dynamicAmplitude', nn='Dynamic  Amplitude', at='float', dv=1);
            cmds.setAttr('gravCTRL.dynamicAmplitude', k=True)
            cmds.expression(s='pvGravAim.translateY=gravCTRL.dynamicAmplitude*-1')
            cmds.setAttr('pvGravArrowShape.overrideEnabled', 1)
            cmds.setAttr('pvGravArrowShape.overrideColor', 6)
            cmds.group('pvGravOrigin', 'pvGravAim_Null', 'gravCTRL', n='gravCTRL_GRP')
            cmds.setAttr('gravCTRL_GRP.translateX', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.translateY', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.translateZ', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.rotateX', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.rotateY', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.rotateZ', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.scaleX', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.scaleY', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.scaleZ', k=False, l=True)
            cmds.setAttr('gravCTRL_GRP.visibility', k=False, l=True)
            for eachNucleus in cmds.ls(type='nucleus'):
                cmds.connectAttr('pvGravOrigin_aimConstraint1.constraintVectorX', '%s.gravityDirectionX' % eachNucleus)
                cmds.connectAttr('pvGravOrigin_aimConstraint1.constraintVectorY', '%s.gravityDirectionY' % eachNucleus)
                cmds.connectAttr('pvGravOrigin_aimConstraint1.constraintVectorZ', '%s.gravityDirectionZ' % eachNucleus)
            cmds.select('gravCTRL');


instanceUI = myUI()
