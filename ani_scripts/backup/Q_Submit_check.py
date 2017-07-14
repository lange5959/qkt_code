# coding=utf-8
import maya.cmds as cmds
import maya.mel as mel
from pymel.core import *
from PySide import QtGui
from PySide import QtCore
import math

# 06302017
print u'开始检查'
cam_name = ''
for i in ls(type='camera'):
    # print i.name()
    # print i.name()
    # print type(i)
    if 'camera' in i.name():
        select(i)
        cmds.pickWalk(direction='up')
        cam = selected()[0]
        # i.getTransform()
        cam_name = cam.name()

cam_start = cam_name.split('_')[-2]
cam_end = cam_name.split('_')[-1]

frange = map(int, (playbackOptions(q=1, min=1), playbackOptions(q=1, max=1)))
if not cmds.currentUnit(q=True, t=True) == 'film':
    # cmds.inViewMessage(amg=u'相机帧速率不对 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0, fontSize=20)
    message = u'<font size="15"><b>相机帧速率不对<\font><br><b>'
    cmds.confirmDialog(title=u'提交检查',
                       message=message,
                       button=['Cancel', 'OK'],
                       defaultButton='OK',
                       cancelButton='Cancel',
                       dismissString='Cancel')
    cmds.error(u"相机帧速率不对")

if int(cam_start) == frange[0]:
    print 'ok'
else:
    # cmds.inViewMessage(amg=u'起始帧与相机不一样 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0,
    #                    fontSize=20)
    message = u'<font size="15"><b>起始帧与相机不一样<\font><br><b>'
    cmds.confirmDialog(title=u'提交检查',
                       message=message,
                       button=['Cancel', 'OK'],
                       defaultButton='OK',
                       cancelButton='Cancel',
                       dismissString='Cancel')
    cmds.error(u"起始帧与相机不一样")

if int(cam_end) == frange[1]:
    print 'ok'
else:
    # cmds.inViewMessage(amg=u'结束帧与相机不一样 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0,
    #                    fontSize=20)
    message = u'<font size="15"><b>结束帧与相机不一样<\font><br><b>'
    cmds.confirmDialog(title=u'提交检查',
                       message=message,
                       button=['Cancel', 'OK'],
                       defaultButton='OK',
                       cancelButton='Cancel',
                       dismissString='Cancel')
    cmds.error(u"结束帧与相机不一样")

# 字幕安全框？
select(cam_name)
cam = selected()[0]

if not cam.getDisplaySafeTitle():
    # cmds.inViewMessage(amg=u'字幕安全框没有打开 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0,
    #                    fontSize=20)
    message = u'<font size="15"><b>字幕安全框没有打开<\font><br><b>'
    cmds.confirmDialog(title=u'提交检查',
                       message=message,
                       button=['Cancel', 'OK'],
                       defaultButton='OK',
                       cancelButton='Cancel',
                       dismissString='Cancel')
    cmds.error(u"字幕安全框没有打开")

# 显示分辨率？
if not cam.getDisplayResolution():
    # cmds.inViewMessage(amg=u'显示分辨率没有打开 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0,
    #                    fontSize=20)
    message = u'<font size="15"><b>显示分辨率没有打开<\font><br><b>'
    cmds.confirmDialog(title=u'提交检查',
                       message=message,
                       button=['Cancel', 'OK'],
                       defaultButton='OK',
                       cancelButton='Cancel',
                       dismissString='Cancel')
    cmds.error(u"显示分辨率没有打开")

# GateMask

if not cam.getDisplayGateMask():
    # cmds.inViewMessage(amg=u'GateMask没有打开 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0,
    #                    fontSize=20)
    message = u'<font size="15"><b>GateMask没有打开<\font><br><b>'
    cmds.confirmDialog(title=u'提交检查',
                       message=message,
                       button=['Cancel', 'OK'],
                       defaultButton='OK',
                       cancelButton='Cancel',
                       dismissString='Cancel')
    cmds.error(u"GateMask没有打开")

# SafeAction

if not cam.getDisplaySafeAction():
    # cmds.inViewMessage(amg=u'SafeAction没有打开 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0,
    #                    fontSize=20)
    message = u'<font size="15"><b>SafeAction没有打开<\font><br><b>'
    cmds.confirmDialog(title=u'提交检查',
                       message=message,
                       button=['Cancel', 'OK'],
                       defaultButton='OK',
                       cancelButton='Cancel',
                       dismissString='Cancel')
    cmds.error(u"SafeAction没有打开")
cam_shape = cam.getShape()
str = 'setAttr "{0}.overscan" 1;'.format(cam_shape)
mel.eval(str)

# 相机锁定

if not cam.tx.isLocked():
    cam.tx.lock()

if not cam.ty.isLocked():
    cam.ty.lock()

if not cam.tz.isLocked():
    cam.tz.lock()

if not cam.rx.isLocked():
    cam.rx.lock()

if not cam.ry.isLocked():
    cam.ry.lock()

if not cam.rz.isLocked():
    cam.rz.lock()

if not cam.sx.isLocked():
    cam.sx.lock()

if not cam.sy.isLocked():
    cam.sy.lock()

if not cam.sz.isLocked():
    cam.sz.lock()

cam_pa = cam.getParent()
cam_pa_list = cam_pa.listRelatives(children=1)
for i in cam_pa_list:

    if i.getShape().name().endswith('aimShape'):
        i.tx.lock()
        i.ty.lock()
        i.tz.lock()
        i.rx.lock()
        i.ry.lock()
        i.rz.lock()

# str(type(selected()[0].getShape())) == "<class 'pymel.core.nodetypes.Locator'>"
# selected()[0].getShape().name().endswith('aimShape')





# 关闭sound
try:
    mel.eval("setSoundDisplay `timeControl -q -s $gPlayBackSlider` 0")
except:
    pass

# 显示层
t = ''
for i in cmds.ls(type='displayLayer'):
    if not i.endswith('defaultLayer'):
        # print i
        t = i
if t:
    if not t == 'noRender':
        message = u'<font size="15"><b>检查noRender层，有多余层<\font><br><b>'
        cmds.confirmDialog(title=u'提交检查',
                           message=message,
                           button=['Cancel', 'OK'],
                           defaultButton='OK',
                           cancelButton='Cancel',
                           dismissString='Cancel')
        cmds.error(u"检查noRender层")

# 第70帧，角色是Tpose
currentTime(70)
all_curve = ls(type='nurbsCurve')
bag = {}
for i in all_curve:
    if 'locater_rootCon' in i.name():
        select(i)  # shape node
        cmds.pickWalk(direction='up')
        obj = selected()[0]
        print obj
        obj_pos = xform(obj, sp=1, q=1, ws=1)
        print obj_pos
        if not math.sqrt(obj_pos[0] ** 2 + obj_pos[1] ** 2 + obj_pos[2] ** 2) < 0.01:
            message = u'<font size="15"><b>在70F不是TPose<\font><br><b>'
            cmds.confirmDialog(title=u'提交检查',
                               message=message,
                               button=['Cancel', 'OK'],
                               defaultButton='OK',
                               cancelButton='Cancel',
                               dismissString='Cancel')
            cmds.error(u"70F 不是TPose")

######
currentTime(101)
select(cl=1)

## 全部显示/隐藏
modelEditor('modelPanel4', edit=True, allObjects=0)
# 只显示模型
modelEditor('modelPanel4', edit=True, polymeshes=1)

mel.eval('setAttr "defaultResolution.width" 2048;')
mel.eval('setAttr "defaultResolution.height" 858;')

# maya.mel.eval('setNamedPanelLayout("Four View")')
mel.eval('setNamedPanelLayout("Single Perspective View")')

perspPanel = cmds.getPanel(withLabel='Persp View')
# editor = cmds.modelEditor()
cmds.modelEditor(perspPanel, edit=True, displayAppearance='wireframe')

select(cam_name)
cam = selected()[0]
cam_name_shape = cam.getShape()
cam_name_shape.name()
cmds.lookThru('perspView', cam_name_shape.name(), nc=100, fc=200)

print '*' * 100
print u'文件检查完毕'
print u'检查项目：\n '
print u'时间条、相机安全框、相机锁定、70F_TPOSE、隐藏控制器'
# message = u'文件检查完毕 -- 检查项目：-- 时间条、Sound、相机安全框、相机锁定、70F_TPOSE、隐藏控制器'
message = u'<font size="15"><b>文件检查完毕 -- 检查项目:</b><br>时间条、Sound、相机安全框、相机锁定、隐藏控制器、摄像机视图、渲染尺寸</font>'
cmds.confirmDialog(title=u'提交检查',
                   message=message,
                   button=['Cancel', 'OK'],
                   defaultButton='OK',
                   cancelButton='Cancel',
                   dismissString='Cancel')

# cmds.inViewMessage(amg=message, pos='midCenter', fade=1, backColor=0x16151515, a=1.0, fontSize=20, fadeStayTime=1000*10)






