# coding:utf-8
import sys
sys.path.append(r'C:\Python27\Lib\site-packages')
sys.path.append(r'Q:\rig\scripts\Q_script')

# from PyQt4 import QtGui
# from PyQt4 import QtCore

from PySide import QtGui
from PySide import QtCore

from pymel.core import *
import maya.cmds as cmds
import random
import os
import utils.generic as generic
reload(generic)
from lib import MyTimer
# from utils.generic import undo_pm
# QtCore.Qt.QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
print os.path.dirname(__file__) + '\Handheld 0703'


class Handheld_camera_shooting(QtGui.QDialog):
    def __init__(self):
        super(Handheld_camera_shooting, self).__init__()
        self.setWindowTitle('Handheld camera shooting')
        self.setMinimumWidth(300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(1200, 50, 250, 150)
        self.setModal(False)

        self.cam_aim_aim_name = ''
        self.cam_aim_cam_name = ''
        self.cam_aim_cam_grp = ''
        self.cam_aim_cam_trans = ''
        self.cam_aim_cam_scale = ''
        self.cam_aim_cam_rot = ''


        main_layout = QtGui.QVBoxLayout(self)

        style_sheet_file = QtCore.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
        style_sheet_file.open(QtCore.QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet_file.readAll()))

        cam_con_move_button = QtGui.QPushButton('Camera Rig')
        main_layout.addWidget(cam_con_move_button)


        create_cam_layout = QtGui.QHBoxLayout()
        self.cam_name_lineedit = QtGui.QLineEdit('camera1')
        self.cteate_cam_button = QtGui.QPushButton('Create Camera')
        self.cteate_cam_button.setMinimumWidth(120)
        self.cteate_cam_button.setObjectName('roundedButton')

        create_cam_layout.addWidget(self.cam_name_lineedit)
        create_cam_layout.addWidget(self.cteate_cam_button)
        # main_layout.addLayout(create_cam_layout)

        mag_layout = QtGui.QHBoxLayout()
        frame_layout = QtGui.QHBoxLayout()
        frame_start_layout = QtGui.QHBoxLayout()
        frame_end_layout = QtGui.QHBoxLayout()
        frame_layout.addLayout(frame_start_layout)
        frame_layout.addLayout(frame_end_layout)
        main_layout.addLayout(frame_layout)
        button_layout = QtGui.QHBoxLayout()


        fre_layout = QtGui.QHBoxLayout()


        frame_start_label = QtGui.QLabel('Frame Start:')
        self.frame_start_lineedit = QtGui.QLineEdit('0')
        frame_start_layout.addWidget(frame_start_label)
        frame_start_layout.addWidget(self.frame_start_lineedit)

        frame_end_label = QtGui.QLabel('Frame End:')
        self.frame_end_lineedit = QtGui.QLineEdit('100')
        frame_end_layout.addWidget(frame_end_label)
        frame_end_layout.addWidget(self.frame_end_lineedit)

        self.mag_label = QtGui.QLabel('Magnitude')
        self.fre_label = QtGui.QLabel('Frame Step')

        self.magnitude_line_edit = QtGui.QLineEdit('0.01')
        self.magnitude_line_edit.setFixedHeight(30)

        mag_layout.addWidget(self.mag_label)
        mag_layout.addWidget(self.magnitude_line_edit)

        self.frequency_line_edit = QtGui.QLineEdit('4')
        self.frequency_line_edit.setFixedHeight(30)
        fre_layout.addWidget(self.fre_label)
        fre_layout.addWidget(self.frequency_line_edit)

        shake_button = QtGui.QPushButton('Key Rot')
        shake_button.setFixedHeight(50)

        trans_button = QtGui.QPushButton('Key Translate')
        trans_button.setFixedHeight(50)

        main_layout.addLayout(mag_layout)
        main_layout.addLayout(fre_layout)

        ##################################################################
        check_layout = QtGui.QHBoxLayout()
        self.rotx_check = QtGui.QCheckBox('X')
        self.rotx_check.setCheckState(QtCore.Qt.Checked)
        self.roty_check = QtGui.QCheckBox('Y')
        self.roty_check.setCheckState(QtCore.Qt.Checked)
        self.rotz_check = QtGui.QCheckBox('Z')
        self.rotz_check.setCheckState(QtCore.Qt.Checked)

        check_layout.addWidget(self.rotx_check)
        check_layout.addWidget(self.roty_check)
        check_layout.addWidget(self.rotz_check)
        main_layout.addLayout(check_layout)

        button_layout.addWidget(shake_button)
        button_layout.addWidget(trans_button)

        main_layout.addLayout(button_layout)

        shake_button.clicked.connect(self.Cam_shake)
        trans_button.clicked.connect(self.Cam_shake_tran)
        self.cteate_cam_button.clicked.connect(self.create_cam)
        cam_con_move_button.clicked.connect(self.cam_con_move)

        self.label = QtGui.QLabel("About Qt MessageBox")
        self.about_button = QtGui.QPushButton('about')
        main_layout.addWidget(self.about_button)
        self.about_button.clicked.connect(self.slotAbout)

    def Cam_shake(self):
        obj = selected()[0]
         # frange = map(int, (playbackOptions(q=1, min=1), playbackOptions(q=1, max=1)))
        start_frame = int(self.frame_start_lineedit.text())
        end_frame = int(self.frame_end_lineedit.text())
        a = float(str(self.magnitude_line_edit.text()))

        b = -a
        step = int(str(self.frequency_line_edit.text()))
        rot_list = []
        for f in range(start_frame, end_frame + 1, step):
            currentTime(f)
            rot = (obj.rx.get(), obj.ry.get(), obj.rz.get())
            rot_list.append(rot)

        n = 0
        undoInfo(openChunk=True)
        for f in range(start_frame, end_frame + 1, step):
            currentTime(f)
            cam_pos_x = 0
            if self.rotx_check.isChecked():
                cam_pos_x = random.uniform(a, b)
            cam_pos_y = 0
            if self.roty_check.isChecked():
                cam_pos_y = random.uniform(a, b)
            cam_pos_z = 0
            if self.rotz_check.isChecked():
                cam_pos_z = random.uniform(a, b)
            # move(obj, (cam_pos_x,cam_pos_y,cam_pos_z), r=1, ws=1)
            obj.rx.set(rot_list[n][0] + cam_pos_x)
            obj.ry.set(rot_list[n][1] + cam_pos_y)
            obj.rz.set(rot_list[n][2] + cam_pos_z)
            obj.r.setKey()
            n += 1
        undoInfo(closeChunk=True)

    def Cam_shake_tran(self):
        obj = selected()[0]
        # frange = map(int, (playbackOptions(q=1, min=1), playbackOptions(q=1, max=1)))
        start_frame = int(self.frame_start_lineedit.text())
        end_frame = int(self.frame_end_lineedit.text())
        a = float(str(self.magnitude_line_edit.text()))

        b = -a
        step = int(str(self.frequency_line_edit.text()))
        trans_list = []
        for f in range(start_frame, end_frame + 1, step):
            currentTime(f)
            trans = (obj.tx.get(), obj.ty.get(), obj.tz.get())
            trans_list.append(trans)

        n = 0
        undoInfo(openChunk=True)
        for f in range(start_frame, end_frame + 1, step):
            currentTime(f)
            cam_pos_x = 0
            if self.rotx_check.isChecked():
                cam_pos_x = random.uniform(a, b)
            cam_pos_y = 0
            if self.roty_check.isChecked():
                cam_pos_y = random.uniform(a, b)
            cam_pos_z = 0
            if self.rotz_check.isChecked():
                cam_pos_z = random.uniform(a, b)
            # move(obj, (cam_pos_x,cam_pos_y,cam_pos_z), r=1, ws=1)
            obj.tx.set(trans_list[n][0] + cam_pos_x)
            obj.ty.set(trans_list[n][1] + cam_pos_y)
            obj.tz.set(trans_list[n][2] + cam_pos_z)
            obj.t.setKey()
            n += 1
        undoInfo(closeChunk=True)

    def create_cam(self):
        undoInfo(openChunk=True)
        cam_name = self.cam_name_lineedit.text()
        obj_cam = camera(name=cam_name)
        obj_cir = circle(nr=(0.0, 10.0, 0.0), name=obj_cam[0].name() + '_con')

        obj_shape = obj_cir[0].getShape()
        cmds.setAttr(obj_shape + ".overrideEnabled", 1)
        cmds.setAttr(obj_shape + ".overrideColor", 17)

        move(obj_cir[0], (0, 0, 0.6), wd=1, os=1)
        obj_cir[0].setScale((2, 2, 2))
        obj_cir[0].setPivots((0, 0, 0), ws=1)
        makeIdentity(obj_cir[0], apply=1, t=1, r=1, s=1, n=1, pn=0)

        parent(obj_cam[0].name(), obj_cir[0].name())
        new_grp = group(em=True, n=obj_cir[0].name() + '_grp')
        parent(obj_cir[0].name(), new_grp.name())
        undoInfo(closeChunk=True)

    # @generic.undo_pm
    def cam_con_move(self):
        cam = selected()[0]
        cam_grp = cam.root()
        cam_aim = 0
        try:
            for i in cam_grp.listRelatives():
                if 'locator' in i.getShape().type():
                    cam_aim = 1
                    self.cam_aim_aim_name = i.name()


        except:
            self.cam_noaim_con(cam)
        if cam_aim:
            for i in cam_grp.listRelatives():
                if 'camera' in i.getShape().type():
                    select(i)
                    cam = selected()[0]
                    self.cam_aim_con(cam)

    def cam_aim_con(self, obj):
        cam = obj
        aim = self.cam_aim_aim_name
        select(aim)
        aim = selected()[0]

        self.cam_aim_cir_con(cam, aim)


    @MyTimer.measure_time
    def cam_noaim_con(self, obj):

        # 针对普通相机
        undoInfo(openChunk=True)

        cam_obj = obj
        # aim cam 相机 的 相机部分加环
        # save data
        cam_scale = cam_obj.scale.get()
        cam_trans = cam_obj.translate.get()
        cam_rot = cam_obj.rotate.get()
        # create circle
        cam_cir = circle(nr=(0.0, 10.0, 0.0), name=cam_obj.name() + '_inside_con')
        cam_cir = cam_cir[0]
        cam_cir.scale.set(cam_scale*1.5)

        # dis = 0.1 * cam_scale
        # for v in cam_cir.cv:
        #     move(v, (0, 0, dis[0]), r=1, os=1)

        cam_cir_shape = cam_cir.getShape()
        setAttr(cam_cir_shape + ".overrideEnabled", 1)
        setAttr(cam_cir_shape + ".overrideColor", 17)

        makeIdentity(cam_cir, apply=1, t=1, s=1, n=1, pn=0)

        setAttr(cam_cir.sx, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.sy, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.sz, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.visibility, lock=1, keyable=0, channelBox=0)
        # 清历史
        delete(cam_cir, ch=1)
        # 给相机的小环打组
        cam_cir_grp = group(em=True, n=cam_cir.name() + '_grp')
        parent(cam_cir, cam_cir_grp)

        # create circle 2
        cam_cir2 = circle(nr=(0.0, 10.0, 0.0), name=cam_obj.name() + '_outside_con')
        cam_cir2 = cam_cir2[0]

        cam_cir2.scale.set(cam_scale * 3)

        # dis = 0.1 * cam_scale
        # for v in cam_cir2.cv:
        #     move(v, (0, 0, dis[0]), r=1, os=1)

        cam_cir2_shape = cam_cir2.getShape()
        setAttr(cam_cir2_shape + ".overrideEnabled", 1)
        setAttr(cam_cir2_shape + ".overrideColor", 17)

        makeIdentity(cam_cir2, apply=1, t=1, s=1, n=1, pn=0)
        delete(cam_cir2, ch=1)
        setAttr(cam_cir2.visibility, lock=1, keyable=0, channelBox=0)
        # 给相机大环打组
        cam_cir2_grp = group(em=True, n=cam_cir2.name() + '_grp')
        parent(cam_cir2, cam_cir2_grp)
        # 小环p给大环
        parent(cam_cir_grp, cam_cir2)
        # to cam's pos
        cir_cons = parentConstraint(cam_obj, cam_cir2_grp, mo=0)
        delete(cir_cons)

        # Constraint
        parentConstraint(cam_cir, cam_obj, mo=1)
        scaleConstraint(cam_cir, cam_obj, mo=1)

        root_grp = group(em=True, n=cam_obj.name() + '_rig_grp')
        parent(cam_cir2_grp, cam_obj, root_grp)
        select(root_grp)
        xform(pivots=cam_trans)

        dis = 0.5 * cam_scale
        for v in cam_cir.cv:
            move(v, (0, 0, dis[0]), r=1, os=1)

        for v in cam_cir2.cv:
            move(v, (0, 0, dis[0]), r=1, os=1)


        undoInfo(closeChunk=True)


    def cam_aim_cir_con(self, cam, aim):
        undoInfo(openChunk=True)

        # aim cam 相机 的 相机部分加环
        cam_obj = cam
        # save data
        cam_scale = cam_obj.scale.get()
        cam_trans = cam_obj.translate.get()
        cam_rot = cam_obj.rotate.get()
        # create circle
        cam_cir = circle(nr=(0.0, 10.0, 0.0), name=cam_obj.name() + '_inside_con')
        cam_cir = cam_cir[0]

        cam_cir.scale.set(cam_scale * 1.5)

        # dis = 0.1 * cam_scale
        # for v in cam_cir.cv:
        #     move(v, (0, 0, dis[0]), r=1, os=1)

        cam_cir_shape = cam_cir.getShape()
        setAttr(cam_cir_shape + ".overrideEnabled", 1)
        setAttr(cam_cir_shape + ".overrideColor", 13)

        makeIdentity(cam_cir, apply=1, t=1, s=1, n=1, pn=0)
        setAttr(cam_cir.rx, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.ry, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.rz, lock=1, keyable=0, channelBox=0)

        setAttr(cam_cir.sx, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.sy, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.sz, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir.visibility, lock=1, keyable=0, channelBox=0)

        delete(cam_cir, ch=1)
        # 给相机的小环打组
        cam_cir_grp = group(em=True, n=cam_cir.name() + '_grp')
        parent(cam_cir, cam_cir_grp)

        # create circle 2
        cam_cir2 = circle(nr=(0.0, 10.0, 0.0), name=cam_obj.name() + '_outside_con')
        cam_cir2 = cam_cir2[0]

        cam_cir2.scale.set(cam_scale * 2.5)

        # dis = 0.1 * cam_scale
        # for v in cam_cir2.cv:
        #     move(v, (0, 0, dis[0]), r=1, os=1)

        cam_cir2_shape = cam_cir2.getShape()
        setAttr(cam_cir2_shape + ".overrideEnabled", 1)
        setAttr(cam_cir2_shape + ".overrideColor", 13)
        # undo    # scale
        setAttr(cam_cir2.rx, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir2.ry, lock=1, keyable=0, channelBox=0)
        setAttr(cam_cir2.rz, lock=1, keyable=0, channelBox=0)
        makeIdentity(cam_cir2, apply=1, t=1, s=1, n=1, pn=0)
        delete(cam_cir2, ch=1)
        setAttr(cam_cir2.visibility, lock=1, keyable=0, channelBox=0)
        # 给相机大环打组
        cam_cir2_grp = group(em=True, n=cam_cir2.name() + '_grp')
        parent(cam_cir2, cam_cir2_grp)
        # 小环p给大环
        parent(cam_cir_grp, cam_cir2)

        # to cam's pos
        cir_cons = parentConstraint(cam_obj, cam_cir2_grp, mo=0)
        delete(cir_cons)
        xform(pivots=cam_trans)

        select(cam_cir_grp)
        xform(pivots=cam_trans, ws=1)

        # Constraint
        pointConstraint(cam_cir, cam_obj, mo=1)
        scaleConstraint(cam_cir, cam_obj, mo=1)

        # part 2 ##########################################################
        # del    # create circle aim
        aim_obj = aim

        aim_cir = circle(nr=(0.0, 10.0, 0.0), name=aim_obj.name() + '_inside_con')
        aim_cir = aim_cir[0]

        aim_cir.scale.set(cam_scale * .8)

        # 改颜色
        aim_cir_shape = aim_cir.getShape()
        setAttr(aim_cir_shape + ".overrideEnabled", 1)
        setAttr(aim_cir_shape + ".overrideColor", 6)
        # 清历史
        makeIdentity(aim_cir, apply=1, t=1, r=1, s=1, n=1, pn=0)
        delete(aim_cir, ch=1)
        setAttr(aim_cir.visibility, lock=1, keyable=0, channelBox=0)
        setAttr(aim_cir.sx, lock=1, keyable=0, channelBox=0)
        setAttr(aim_cir.sy, lock=1, keyable=0, channelBox=0)
        setAttr(aim_cir.sz, lock=1, keyable=0, channelBox=0)

        aim_cir_grp = group(em=True, n=aim_cir.name() + '_grp')
        parent(aim_cir, aim_cir_grp)

        # create circle 2
        aim_cir2 = circle(nr=(0.0, 10.0, 0.0), name=aim_obj.name() + '_outside_con')
        aim_cir2 = aim_cir2[0]

        aim_cir2_shape = aim_cir2.getShape()
        setAttr(aim_cir2_shape + ".overrideEnabled", 1)
        setAttr(aim_cir2_shape + ".overrideColor", 6)
        #redo    # scale

        aim_cir2.scale.set(cam_scale * 1.5)

        makeIdentity(aim_cir2, apply=1, t=1, r=1, s=1, n=1, pn=0)
        delete(aim_cir2, ch=1)
        setAttr(aim_cir2.visibility, lock=1, keyable=0, channelBox=0)
        setAttr(aim_cir2.sx, lock=1, keyable=0, channelBox=0)
        setAttr(aim_cir2.sy, lock=1, keyable=0, channelBox=0)
        setAttr(aim_cir2.sz, lock=1, keyable=0, channelBox=0)

        aim_cir2_grp = group(em=True, n=aim_obj.name() + '_grp')
        parent(aim_cir2, aim_cir2_grp)
        # 小环p给大环
        parent(aim_cir_grp, aim_cir2)

        # undo    # to aim's pos
        cir_cons = parentConstraint(aim_obj, aim_cir2_grp, mo=0)
        delete(cir_cons)
        # Constraint
        parentConstraint(aim_cir, aim_obj, mo=1)

        # part 3 #######################################
        # 创建大环
        root_cir = circle(nr=(0.0, 10.0, 0.0), name=cam_obj.name() + '_root_con')
        root_cir = root_cir[0]
        root_cir.scale.set(cam_scale * 4)

        # dis = 0.1 * cam_scale
        # for v in root_cir.cv:
        #     move(v, (0, 0, dis[0]), r=1, os=1)
        # color
        root_cir_shape = root_cir.getShape()
        setAttr(root_cir_shape + ".overrideEnabled", 1)
        setAttr(root_cir_shape + ".overrideColor", 17)

        makeIdentity(root_cir, apply=1, t=1, r=1, s=1, n=1, pn=0)
        delete(root_cir, ch=1)

        setAttr(root_cir.visibility, lock=1, keyable=0, channelBox=0)

        root_cir_grp = group(em=True, n=root_cir.name() + '_grp')
        parent(root_cir, root_cir_grp)

        cir_cons = parentConstraint(cam_obj, root_cir_grp, mo=0)
        delete(cir_cons)
        # 俩组P 给大环
        parent(aim_cir2_grp, cam_cir2_grp, root_cir)

        # 最后打组
        cam_grp = cam_obj.root()
        select(cam_grp)
        xform(pivots=cam_trans)
        root_root_grp = group(em=True, n=cam_obj.name() + '_rig_grp')
        parent(root_cir_grp, cam_grp, root_root_grp)
        select(root_root_grp)
        xform(pivots=cam_trans)

        dis = 0.5 * cam_scale
        for v in cam_cir.cv:
            move(v, (0, 0, dis[0]), r=1, os=1)

        for v in cam_cir2.cv:
            move(v, (0, 0, dis[0]), r=1, os=1)

        for v in root_cir.cv:
            move(v, (0, 0, dis[0]), r=1, os=1)


        undoInfo(closeChunk=True)


    def slotAbout(self):
        path = os.path.dirname(__file__)+'/about.txt'
        f = open(path, 'r')
        data = f.read()

        # data = translator.tr(data)
        # print help(translator)
        # installTranslator(translator)
        # print data
        # print f
        # filename = unicode.translate(data)

        QtGui.QMessageBox.about(self, "About", data.decode("utf-8"))
        f.close()
        # msgBox = QtGui.QMessageBox()
        # msgBox.setText("The document has been modified.")
        # print os.path.dirname(__file__)
        # os.system((os.path.dirname(__file__)+'/about.txt'))
        self.label.setText("About MessageBox")



Handheld_camera_shooting = Handheld_camera_shooting()
Handheld_camera_shooting.show()

# import Handheld_camera_shooting
# reload(Handheld_camera_shooting)
# dog = Handheld_camera_shooting.Handheld_camera_shooting()
# dog.show()



