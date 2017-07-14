# coding=utf-8
# auther: mengwei
import sys
import os
from Qt import QtWidgets, QtCore, QtGui
import pymel.core as pm
import maya.cmds as cmds
# lightingManager
from functools import partial
import json
import time
import logging


try:
    pm.loadPlugin('mtoa.mll')
except:
    cmds.error("cant find mtoa")

logging.basicConfig()
logger = logging.getLogger('LightingManager')
logger.setLevel(logging.DEBUG)

class Lightmanager(QtWidgets.QDialog):

    lightTypes = {
        "Point Light": partial(pm.shadingNode, 'pointLight', asLight=True),
        "Spot Light": partial(pm.shadingNode, 'spotLight', asLight=True),
        "Directional Light": partial(pm.shadingNode, 'directionalLight', asLight=True),
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight=True),
        # shadingNode -asLight areaLight
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight=True),
        "aiAreaLight": partial(pm.shadingNode, 'aiAreaLight', asLight=True),
        "aiSkyDomeLight": partial(pm.shadingNode, 'aiSkyDomeLight', asLight=True),
        "aiPhotometricLight": partial(pm.shadingNode, 'aiPhotometricLight', asLight=True),

    }

    # "aiAreaLight": partial(pm.shadingNode, 'aiAreaLight', asLight=True, name='aiAreaLight'),
    # "aiSkyDomeLight": partial(pm.shadingNode, 'aiSkyDomeLight', asLight=True, name='aiSkyDomeLight'),
    # "aiPhotometricLight": partial(pm.shadingNode, 'aiPhotometricLight', asLight=True, name='aiPhotometricLight')

    def __init__(self):
        """
        light tool
        """
        super(Lightmanager, self).__init__()
        self.setWindowTitle('Lighting Manager')

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(120, 100, 250, 150)
        self.setModal(False)


        style_sheet_file = QtCore.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
        style_sheet_file.open(QtCore.QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet_file.readAll()))

        self.buildUI()
        self.populate()
        self.lightGroup = []

    def populate(self):
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(False)
                widget.deleteLater()

        # 'aiAreaLight', "aiSkyDomeLight", "aiPhotometricLight"
        for light in pm.ls(type=["areaLight", "spotLight", "pointLight", "directionalLight",
                                 "volumeLight", "aiAreaLight", "aiSkyDomeLight", "aiPhotometricLight"]):
            light = light.getParent()  # shape -> transform
            self.addLight(light)

    def buildUI(self):

        layout = QtWidgets.QVBoxLayout(self)

        create_layout = QtWidgets.QHBoxLayout()
        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in sorted(self.lightTypes):
            self.lightTypeCB.addItem(lightType)
        create_layout.addWidget(self.lightTypeCB)

        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        create_layout.addWidget(createBtn)

        self.connect_button = QtWidgets.QPushButton("connect")
        self.connect_button.clicked.connect(self.light_group)
        create_layout.addWidget(self.connect_button)

        layout.addLayout(create_layout)

        label_grid_lyt = QtWidgets.QGridLayout()

        self.viz = QtWidgets.QLabel("Visibility")
        self.viz.setMaximumWidth(60)
        label_grid_lyt.addWidget(self.viz, 1, 0)

        self.name = QtWidgets.QLabel("Name")
        self.name.setMaximumWidth(70)
        label_grid_lyt.addWidget(self.name, 1, 1)

        self.int = QtWidgets.QLabel("Int")
        self.int.setMaximumWidth(50)
        label_grid_lyt.addWidget(self.int, 1, 2)

        self.sel = QtWidgets.QLabel("Sel")
        self.sel.setMaximumWidth(50)
        label_grid_lyt.addWidget(self.sel, 1, 3)

        self.solo = QtWidgets.QLabel("solo")
        self.solo.setMaximumWidth(75)
        label_grid_lyt.addWidget(self.solo, 1, 4)

        self.dele = QtWidgets.QLabel("del")
        label_grid_lyt.addWidget(self.dele, 1, 5)



        layout.addLayout(label_grid_lyt)


        # scrollWidget

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)
        title_widget = TitleWidget()
        self.scrollLayout.addWidget(title_widget)

        # widget = LightWidget(light)
        # self.scrollLayout.addWidget(widget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea)

        save_layout = QtWidgets.QHBoxLayout()
        saveBtn = QtWidgets.QPushButton('save')
        saveBtn.clicked.connect(self.saveLights)
        save_layout.addWidget(saveBtn)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.importLights)
        save_layout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton("Refresh")
        refreshBtn.clicked.connect(self.populate)
        save_layout.addWidget(refreshBtn)

        layout.addLayout(save_layout)

        about_button = QtWidgets.QPushButton('About')
        layout.addWidget(about_button)

        about_button.clicked.connect(self.slotAbout)

    def saveLights(self):
        path = pm.sceneName()
        if path == '':
            cmds.error('Please save first')
        name = os.path.basename(path)
        name = 'light_' + name
        path = os.path.dirname(path)
        path = path.split('/')
        path.append('light')
        path.append(name)
        path = '/'.join(path)
        light_dir = os.path.dirname(path)
        try:
            os.mkdir(light_dir)
        except:
            pass
        # path = r'D:/temp/a04.ma'
        cmds.file(path, force=True, exportSelected=True, type="mayaAscii")
        cmds.inViewMessage(amg=u'保存完毕 <hl>!!!</hl>.', pos='midCenter', fade=1, backColor=0x16151515, a=1.0, fontSize=20)
        #
        properties = {}

        for lightWidget in self.findChildren(LightWidget):
            light = lightWidget.light
            print light, type(light)
            # transform = light.getTransform()

            properties[str(light)] = {

                'translate': list(light.translate.get()),
                'rotate': list(light.rotate.get()),
                'lightType': pm.objectType(light.getShape()),
                'intensity': light.intensity.get(),
                'color': light.color.get()
            }
        directory = self.getDirectory()
        lightFile = os.path.join(directory, 'lightFile_%s.json' % time.strftime('%m%d'))
        with open(lightFile, 'w') as f:
            json.dump(properties, f, indent=4)

        logger.info('Saving file to %s' % lightFile)

    def getDirectory(self):
        directory = os.path.join(pm.internalVar(userAppDir=True), 'lightManager')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def importLights(self):
        directory = self.getDirectory()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Light Browser", directory)
        with open(fileName[0], 'r') as f:
            properties = json.load(f)

        # pprint.pprint(properties)
        for light, info in properties.items():
            lightType = info.get('lightType')
            for lt in self.lightTypes:
                if ("%sLight" % lt.split()[0].lower()) == lightType:
                    break
                # lt = "%sLight" % lt.split()[0].lower()
                # if lt == lightType:
                #     break
            else:
                logger.info('Cannot find a corresponding light type for %s (%s)' % (light, lightType))
                continue

            light = self.createLight(lightType=lt)
            print light, type(light), '*'*100
            light_shape = light.getShape()
            # light.set(info.get('intensity'))
            pm.setAttr(light_shape+'.intensity', info.get('intensity'))

            light.color.set(info.get('color'))

            light.translate.set(info.get('translate'))
            # light.rotate.set(info.get('rotation'))
            # pm.setAttr(light.name()+'.setRotation', info.get('rotate'))
            light.setRotation(info.get('rotate'))
        self.populate()


    def createLight(self, lightType=None, add=True):
        if not lightType:
            lightType = self.lightTypeCB.currentText()
        func = self.lightTypes[lightType]

        light = func()
        if add:
            self.addLight(light)
        return light

    def addLight(self, light):
        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)
        widget.solo.connect(self.onSolo)

    def onSolo(self, value):
        lightWidgets = self.findChildren(LightWidget)
        # pprint.pprint(lightWidgets)
        for widget in lightWidgets:
            if widget != self.sender():  # signal sourceobject
                widget.disableLight(value)
    def light_group(self):
        for light in pm.selected():
            self.lightGroup.append(light.name())
            print light.name()
        widget = Connect_widget(self.lightGroup)
        self.scrollLayout.addWidget(widget)
        self.lightGroup = []

    def slotAbout(self):
        path = os.path.dirname(__file__) + '/Q_light_tool.txt'
        f = open(path, 'r')
        data = f.read()

        QtWidgets.QMessageBox.about(self, "About", data.decode("utf-8"))
        f.close()



# child
class LightWidget(QtWidgets.QWidget):
    solo = QtCore.Signal(bool)
    def __init__(self, light):
        super(LightWidget, self).__init__()
        if isinstance(light, basestring):
            light = pm.PyNode(light)
        self.light = light

        light_shape = self.light.getShape()
        if light_shape.type().startswith('ai'):
            self.build_ar_UI()
        else:
            self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        # name & check vis
        self.name = QtWidgets.QCheckBox('.')
        self.name.setMaximumWidth(80)
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.visibility.set(val))
        layout.addWidget(self.name, 0, 0)
        # rename
        self.renameLin = QtWidgets.QLineEdit(str(self.light.name()))
        self.renameLin.setMinimumWidth(80)
        # self.renameLin.setMaximumWidth(80)
        self.renameLin.setMaximumHeight(20)
        self.renameLin.textChanged.connect(self.renameLight)
        layout.addWidget(self.renameLin, 0, 1)
        # intensity
        intensity = pm.getAttr(self.light.name() + '.intensity')
        intensity = round(intensity, 2)
        self.intensityLin = QtWidgets.QLineEdit(str(intensity))
        self.intensityLin.setMaximumWidth(50)
        self.intensityLin.setMaximumHeight(20)
        # self.intensityLin.selectAll()
        self.intensityLin.setFocus()
        self.intensityLin.textChanged.connect(self.intensity)
        layout.addWidget(self.intensityLin, 0, 2)

        # select
        self.selBtn = QtWidgets.QPushButton('#')
        self.selBtn.setMaximumWidth(50)
        self.selBtn.setCheckable(True)
        # self.selBtn.setMaximumWidth(20)
        self.selBtn.setMaximumHeight(20)
        self.selBtn.toggled.connect(self.selectlight)
        # self.selBtn.clicked.connect(self.selectlight)
        layout.addWidget(self.selBtn, 0, 3)
        # solo
        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setMaximumWidth(75)
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.solo.emit(val))
        layout.addWidget(soloBtn, 0, 4)
        # del
        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 5)
        # slider
        # intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # intensity.setMinimum(1.0)
        # intensity.setMaximum(10.0)
        # intensity.setRange(0.0, 10.0)
        # intensity.setValue(self.light.intensity.get())
        # intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        # layout.addWidget(intensity, 1, 0, 1, 2)

        # color
        self.colorBtn = QtWidgets.QPushButton('C')
        self.colorBtn.setMaximumWidth(30)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 0, 6)

        # shadow color
        self.shadowcolorBtn = QtWidgets.QPushButton('Shadow')
        self.shadowcolorBtn.setMaximumWidth(60)
        self.shadowcolorBtn.setMaximumHeight(20)
        self.setShadowButtonColor()
        self.shadowcolorBtn.clicked.connect(self.setShadowColor)
        layout.addWidget(self.shadowcolorBtn, 0, 7)

        # emitDiffuse & check
        self.emitDiffuse = QtWidgets.QCheckBox('Dif')
        self.emitDiffuse.setChecked(self.light.emitDiffuse.get())
        self.emitDiffuse.toggled.connect(lambda val: self.light.emitDiffuse.set(val))
        layout.addWidget(self.emitDiffuse, 0, 8)

        # emitDiffuse & check
        self.emitSpecular = QtWidgets.QCheckBox('Spe')
        self.emitSpecular.setChecked(self.light.emitSpecular.get())
        self.emitSpecular.toggled.connect(lambda val: self.light.emitSpecular.set(val))
        layout.addWidget(self.emitSpecular, 0, 9)
        # Illuminates by default & check
        self.light_connect = QtWidgets.QCheckBox('Illum')
        self.light_ibd_check = self.light_ibd()
        self.light_connect.setChecked(self.light_ibd_check)
        self.light_connect.toggled.connect(self.light_ibd_set)
        layout.addWidget(self.light_connect, 0, 10)

        # exp_label
        self.exp_label = QtWidgets.QLabel('Exposure:')
        layout.addWidget(self.exp_label, 0, 11)
        # exp
        ai_exp = pm.getAttr(self.light.name() + '.aiExposure')
        ai_exp = round(ai_exp, 2)
        self.expLin = QtWidgets.QLineEdit(str(ai_exp))
        self.expLin.setMaximumWidth(40)
        self.expLin.setMaximumHeight(20)
        self.expLin.textChanged.connect(self.exposure_set)
        layout.addWidget(self.expLin, 0, 12)


        # Sample
        self.sam_label = QtWidgets.QLabel('Sample:')
        layout.addWidget(self.sam_label, 0, 13)

        # sample aiSamples
        ai_sample = pm.getAttr(self.light.name() + '.aiSamples')
        ai_sample = round(ai_sample, 2)
        self.samLin = QtWidgets.QLineEdit(str(ai_sample))
        self.samLin.setMaximumWidth(40)
        self.samLin.setMaximumHeight(20)
        self.samLin.textChanged.connect(self.sample_set)
        layout.addWidget(self.samLin, 0, 14)

        if self.light.hasAttr('aiAngle'):
            # aiAngle
            self.angle_label = QtWidgets.QLabel('aiAngle:')
            layout.addWidget(self.angle_label, 0, 15)

            #
            ai_angle = pm.getAttr(self.light.name() + '.aiAngle')
            ai_angle = round(ai_angle, 2)
            self.aiangleLin = QtWidgets.QLineEdit(str(ai_angle))
            self.aiangleLin.setMaximumWidth(40)
            self.aiangleLin.setMaximumHeight(20)
            self.aiangleLin.textChanged.connect(self.angle_set)
            layout.addWidget(self.aiangleLin, 0, 16)


    def build_ar_UI(self):

        layout = QtWidgets.QGridLayout(self)
        # name & check vis
        self.name = QtWidgets.QCheckBox('.')
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.visibility.set(val))
        layout.addWidget(self.name, 0, 0)

        # rename
        self.renameLin = QtWidgets.QLineEdit(str(self.light.name()))
        self.renameLin.setMinimumWidth(60)
        self.renameLin.setMaximumHeight(20)
        self.renameLin.textChanged.connect(self.renameLight)
        layout.addWidget(self.renameLin, 0, 1)

        # intensity
        ai_intensity = pm.getAttr(self.light.name() + '.intensity')
        ai_intensity = round(ai_intensity, 2)
        self.intensityLin = QtWidgets.QLineEdit(str(ai_intensity))
        self.intensityLin.setMaximumWidth(60)
        self.intensityLin.setMaximumHeight(20)
        # self.intensityLin.selectAll()
        self.intensityLin.setFocus()
        self.intensityLin.textChanged.connect(self.intensity)
        layout.addWidget(self.intensityLin, 0, 2)

        # select
        self.selBtn = QtWidgets.QPushButton('AR')
        self.selBtn.setCheckable(True)
        self.selBtn.setMaximumWidth(40)
        self.selBtn.setMaximumHeight(30)
        self.selBtn.toggled.connect(self.selectlight)
        # self.selBtn.clicked.connect(self.selectlight)
        layout.addWidget(self.selBtn, 0, 3)
        # solo
        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.solo.emit(val))
        layout.addWidget(soloBtn, 0, 4)
        # del
        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 5)

        # color
        self.colorBtn = QtWidgets.QPushButton('C')
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 0, 6)

        # shadow color
        self.ai_shadowcolorBtn = QtWidgets.QPushButton('Shadow')
        self.ai_shadowcolorBtn.setMaximumWidth(60)
        self.ai_shadowcolorBtn.setMaximumHeight(20)
        self.setAiShadowButtonColor()
        self.ai_shadowcolorBtn.clicked.connect(self.setAiShadowColor)
        layout.addWidget(self.ai_shadowcolorBtn, 0, 7)
        # slider
        # intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # intensity.setMinimum(1.0)
        # intensity.setMaximum(10.0)
        # intensity.setRange(0.0, 10.0)
        # intensity.setValue(self.light.intensity.get())
        # intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        # layout.addWidget(intensity, 1, 0, 1, 2)
        # int_label
        # self.intensity_label = QtWidgets.QLabel('Intensity:')
        # layout.addWidget(self.intensity_label, 1, 3)

        # exp_label
        self.exp_label = QtWidgets.QLabel('Exposure:')
        layout.addWidget(self.exp_label, 0, 8)
        # exp
        ai_exp = pm.getAttr(self.light.name() + '.aiExposure')
        ai_exp = round(ai_exp, 2)
        self.expLin = QtWidgets.QLineEdit(str(ai_exp))
        self.expLin.setMaximumWidth(40)
        self.expLin.setMaximumHeight(20)
        self.expLin.textChanged.connect(self.exposure_set)
        layout.addWidget(self.expLin, 0, 9)

        # sam_label
        self.sam_label = QtWidgets.QLabel('Sample:')
        layout.addWidget(self.sam_label, 0, 10)

        # sample aiSamples
        ai_sample = pm.getAttr(self.light.name() + '.aiSamples')
        ai_sample = round(ai_sample, 2)
        self.samLin = QtWidgets.QLineEdit(str(ai_sample))
        self.samLin.setMaximumWidth(40)
        self.samLin.setMaximumHeight(20)
        self.samLin.textChanged.connect(self.sample_set)
        layout.addWidget(self.samLin, 0, 11)


    def build_connect_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        self.my_com = QtWidgets.QComboBox()
        layout.addWidget(self.my_com)

        self.my_com.addItem(u'd')
        self.my_com.addItem(u'a')


    def sample_set(self, val):
        val = float(val)
        # light = self.light.aiSamples
        # light = str(light)
        pm.setAttr(self.light.name() + '.aiSamples', val)

    def angle_set(self, val):
        val = float(val)
        pm.setAttr(self.light.name() + '.aiAngle', val)


    def intensity(self, val):
        val = float(val)
        val = round(val, 2)
        # print val,type(val)
        # self.light.intensity.set(val)
        pm.setAttr(self.light.name() + '.intensity', val)

    def exposure_set(self, val):
        val = float(val)
        # light = self.light.aiExposure
        # light = str(light)
        # pm.setAttr(light, val)
        pm.setAttr(self.light.name() + '.aiExposure', val)

    def selectlight(self, val):
        if val:
            pm.select(self.light, add=True)
        else:
            pm.select(cl=True)

    def setButtonColor(self, color=None):
        if not color:
            color = self.light.color.get()

        assert len(color) == 3, "You must provide a list of 3 colors"

        r, g, b = [c * 255 for c in color]

        self.colorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 255)' % (r, g, b))

    def setShadowButtonColor(self, color=None):
        if not color:
            color = self.light.shadowColor.get()
            # print 'shadowColor', color

        assert len(color) == 3, "You must provide a list of 3 colors"

        r, g, b = [c * 255 for c in color]

        self.shadowcolorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 255)' % (r, g, b))

    def setColor(self):
        shadowColor = self.light.color.get()
        color = pm.colorEditor(rgbValue=shadowColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)

        # self.light.color.set(color)
        pm.setAttr(self.light.name() + '.color', color)
        self.setButtonColor(color)

    def setShadowColor(self):
        shadowColor = self.light.shadowColor.get()
        color = pm.colorEditor(rgbValue=shadowColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)
        # self.light.shadowColor.set(color)
        pm.setAttr(self.light.name() + '.shadowColor', color)
        self.setShadowButtonColor(color)

    def disableLight(self, value):
        self.name.setChecked(not value)

    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()
        pm.delete(self.light)

    def renameLight(self, newname):
        pm.rename(self.light, newname)

    def light_ibd(self):
        name = self.light
        light_instObjGroups = str(self.light.name()) + '.instObjGroups'
        if cmds.connectionInfo(light_instObjGroups, isSource=True):
            return 1
        else:
            return 0

    def light_ibd_set(self, check):
        # illuminate by default
        print check
        name = self.light
        dagSetMembers = ''
        light_instObjGroups = str(self.light.name()) + '.instObjGroups'
        if check:
            cmds.connectAttr(light_instObjGroups, 'defaultLightSet.dagSetMembers', nextAvailable=1, )
        else:
            if cmds.connectionInfo(light_instObjGroups, isSource=True):
                destinations = cmds.connectionInfo(light_instObjGroups, destinationFromSource=True)
                for destination in destinations:
                    dagSetMembers = destination
                    print dagSetMembers
            cmds.disconnectAttr(light_instObjGroups, dagSetMembers)

    def get_light_intensity(self):
        mystr = self.light.name() + '.intensity'
        return pm.getAttr(mystr)

    def setAiShadowColor(self):
        my_str = self.light.name() + ".aiShadowColor"
        shadowColor = pm.getAttr(my_str)
        # shadowColor = self.light.shadowColor.get()
        color = pm.colorEditor(rgbValue=shadowColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)
        pm.setAttr(my_str, color)
        self.setAiShadowButtonColor(color)

    def setAiShadowButtonColor(self, color=None):
        my_str = self.light.name() + ".aiShadowColor"
        if not color:
            # color = self.light.shadowColor.get()
            color = pm.getAttr(my_str)
            # print 'shadowColor', color

        assert len(color) == 3, "You must provide a list of 3 colors"

        r, g, b = [c * 255 for c in color]

        self.ai_shadowcolorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 255)' % (r, g, b))

# fixme // del later
class TitleWidget(QtWidgets.QWidget):
    def __init__(self):
        super(TitleWidget, self).__init__()

        self.buildUI()


    def buildUI(self):
        label_grid_lyt = QtWidgets.QGridLayout(self)

        self.viz = QtWidgets.QLabel("Viz")
        label_grid_lyt.addWidget(self.viz, 0, 0)

        self.viz = QtWidgets.QLabel("Name")
        label_grid_lyt.addWidget(self.viz, 0, 1)

        self.viz = QtWidgets.QLabel("Sel")
        label_grid_lyt.addWidget(self.viz, 0, 2)

        self.viz = QtWidgets.QLabel("solo")
        label_grid_lyt.addWidget(self.viz, 0, 3)

        self.viz = QtWidgets.QLabel("del")
        label_grid_lyt.addWidget(self.viz, 0, 4)

        self.viz = QtWidgets.QLabel("Int")
        label_grid_lyt.addWidget(self.viz, 0, 5)


class Connect_widget(QtWidgets.QWidget):

    def __init__(self, lights_list):
        super(Connect_widget, self).__init__()
        self.lights_list = lights_list

        pm.select(self.lights_list[0])
        self.light_sel = pm.selected()[0]
        light_shape = self.light_sel.getShape()
        if light_shape.type().startswith('ai'):
            self.build_ar_UI()
        else:
            self.buildUI()

        # self.buildUI()
        # layout = QtWidgets.QHBoxLayout(self)

        self.add_item()

        self.light = ''




    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        # name & check vis
        self.name = QtWidgets.QCheckBox('.')
        self.name.setChecked(True)
        self.name.toggled.connect(self.list_vis)
        layout.addWidget(self.name, 0, 0)

        self.my_com = QtWidgets.QComboBox()
        self.my_com.setMaximumWidth(60)
        layout.addWidget(self.my_com, 0, 1)
        # rename
        # self.renameLin = QtWidgets.QLineEdit(str(self.light.name()))
        # self.renameLin.setMaximumWidth(80)
        # self.renameLin.setMaximumHeight(20)
        # self.renameLin.textChanged.connect(self.renameLight)
        # layout.addWidget(self.renameLin, 0, 1)
        # intensity
        # intensity = pm.getAttr(self.light.name() + '.intensity')
        # intensity = round(intensity, 2)
        self.intensityLin = QtWidgets.QLineEdit('1')
        self.intensityLin.setMaximumWidth(40)
        self.intensityLin.setMaximumHeight(20)
        # self.intensityLin.selectAll()
        self.intensityLin.setFocus()

        self.intensityLin.returnPressed.connect(self.list_intensity)
        layout.addWidget(self.intensityLin, 0, 2)
        #
        # # select
        # self.selBtn = QtWidgets.QPushButton('#')
        # self.selBtn.setCheckable(True)
        # self.selBtn.setMaximumWidth(20)
        # self.selBtn.setMaximumHeight(20)
        # self.selBtn.toggled.connect(self.selectlight)
        # # self.selBtn.clicked.connect(self.selectlight)
        # layout.addWidget(self.selBtn, 0, 3)
        # # solo
        # soloBtn = QtWidgets.QPushButton('Solo')
        # soloBtn.setCheckable(True)
        # soloBtn.toggled.connect(lambda val: self.solo.emit(val))
        # layout.addWidget(soloBtn, 0, 4)
        # # del
        # deleteBtn = QtWidgets.QPushButton('X')
        # deleteBtn.clicked.connect(self.deleteLight)
        # deleteBtn.setMaximumWidth(10)
        # layout.addWidget(deleteBtn, 0, 5)
        # # slider
        # # intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # # intensity.setMinimum(1.0)
        # # intensity.setMaximum(10.0)
        # # intensity.setRange(0.0, 10.0)
        # # intensity.setValue(self.light.intensity.get())
        # # intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        # # layout.addWidget(intensity, 1, 0, 1, 2)
        #
        # color
        self.colorBtn = QtWidgets.QPushButton('C')
        self.colorBtn.setMaximumWidth(30)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 0, 3)
        #
        # shadow color
        self.shadowcolorBtn = QtWidgets.QPushButton('Shadow')
        self.shadowcolorBtn.setMaximumWidth(60)
        self.shadowcolorBtn.setMaximumHeight(20)
        self.setShadowButtonColor()
        self.shadowcolorBtn.clicked.connect(self.setShadowColor)
        layout.addWidget(self.shadowcolorBtn, 0, 4)
        #
        # emitDiffuse & check
        self.emitDiffuse = QtWidgets.QCheckBox('Dif')
        # self.emitDiffuse.setChecked()
        self.emitDiffuse.toggled.connect(self.list_Dif)
        layout.addWidget(self.emitDiffuse, 0, 5)
        #
        # emitSpecular & check
        self.emitSpecular = QtWidgets.QCheckBox('Spe')
        self.emitSpecular.setChecked(1)
        self.emitSpecular.toggled.connect(self.list_Spe)
        layout.addWidget(self.emitSpecular, 0, 6)
        # Illuminates by default & check
        self.light_connect = QtWidgets.QCheckBox('Illum')
        self.light_ibd_check = self.light_ibd()
        self.light_connect.setChecked(self.light_ibd_check)
        self.light_connect.toggled.connect(self.light_ibd_set)
        layout.addWidget(self.light_connect, 0, 7)

    def add_item(self):
        for i in self.lights_list:
            light_name = i
            self.my_com.addItem(light_name)
            pm.select(i)
        self.light = self.my_com.currentIndex()

    def build_ar_UI(self):
        layout = QtWidgets.QGridLayout(self)
        # name & check vis
        self.name = QtWidgets.QCheckBox('.')
        self.name.setChecked(0)
        self.name.toggled.connect(self.ai_list_vis)
        layout.addWidget(self.name, 0, 0)

        self.my_com = QtWidgets.QComboBox()
        self.my_com.setMaximumWidth(60)
        layout.addWidget(self.my_com, 0, 1)

        # int_label
        self.intensity_label = QtWidgets.QLabel('Intensity:')
        layout.addWidget(self.intensity_label, 0, 2)

        # intensity
        # ai_intensity = pm.getAttr(self.light.name() + '.intensity')
        # ai_intensity = round(ai_intensity, 2)
        self.intensityLin = QtWidgets.QLineEdit('1')
        self.intensityLin.setMaximumWidth(60)
        self.intensityLin.setMaximumHeight(20)
        self.intensityLin.returnPressed.connect(self.ai_list_intensity)
        layout.addWidget(self.intensityLin, 0, 3)
        # color
        self.colorBtn = QtWidgets.QPushButton('C')
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 0, 4)

        # shadow color
        self.ai_shadowcolorBtn = QtWidgets.QPushButton('Shadow')
        self.ai_shadowcolorBtn.setMaximumWidth(60)
        self.ai_shadowcolorBtn.setMaximumHeight(20)
        self.setAiShadowButtonColor()
        self.ai_shadowcolorBtn.clicked.connect(self.setAiShadowColor)
        layout.addWidget(self.ai_shadowcolorBtn, 0, 5)


        # exp_label
        self.exp_label = QtWidgets.QLabel('Exposure:')
        layout.addWidget(self.exp_label, 0, 6)
        # exp
        # ai_exp = pm.getAttr(self.light.name() + '.aiExposure')
        # ai_exp = round(ai_exp, 2)
        self.expLin = QtWidgets.QLineEdit('1')
        self.expLin.setMaximumWidth(40)
        self.expLin.setMaximumHeight(20)
        self.expLin.textChanged.connect(self.exposure_set)
        layout.addWidget(self.expLin, 0, 7)
        #
        # sam_label
        self.sam_label = QtWidgets.QLabel('Sample:')
        layout.addWidget(self.sam_label, 0, 8)
        #
        # sample aiSamples
        # ai_sample = pm.getAttr(self.light.name() + '.aiSamples')
        # ai_sample = round(ai_sample, 2)
        self.samLin = QtWidgets.QLineEdit('1')
        self.samLin.setMaximumWidth(40)
        self.samLin.setMaximumHeight(20)
        self.samLin.textChanged.connect(self.sample_set)
        layout.addWidget(self.samLin, 0, 9)

    def list_vis(self, val):
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            light = pm.selected()[0].visibility.set(val)
    def ai_list_vis(self, val):
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            light = pm.selected()[0].visibility.set(val)

    def list_intensity(self):
        val = self.intensityLin.text()
        val = float(val)
        val = round(val, 2)
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            light = pm.selected()[0].intensity.set(val)
    def ai_list_intensity(self):
        val = self.intensityLin.text()
        val = float(val)
        val = round(val, 2)
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            # light = pm.selected()[0].intensity.set(val)
            light = pm.selected()[0].name()
            pm.setAttr(light + '.intensity', val)

    def setButtonColor(self, color=None):
        if not color:
            # color = pm.selected()[0].color.get()
            light = pm.selected()[0].name()
            color = pm.getAttr(light + '.color')

        assert len(color) == 3, "You must provide a list of 3 colors"

        r, g, b = [c * 255 for c in color]

        self.colorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 255)' % (r, g, b))

    def setShadowButtonColor(self, color=None):
        if not color:
            color = pm.selected()[0].color.get()
            # print 'shadowColor', color

        assert len(color) == 3, "You must provide a list of 3 colors"

        r, g, b = [c * 255 for c in color]

        self.shadowcolorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 255)' % (r, g, b))

    def setAiShadowButtonColor(self, color=None):

        my_str = self.lights_list[0] + ".aiShadowColor"
        if not color:
            color = pm.getAttr(my_str)
            # print 'shadowColor', color

        assert len(color) == 3, "You must provide a list of 3 colors"

        r, g, b = [c * 255 for c in color]

        self.ai_shadowcolorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 255)' % (r, g, b))

    def setShadowColor(self):

        light = self.lights_list[0]
        pm.select(light)
        light = pm.selected()[0]

        shadowColor = light.shadowColor.get()
        color = pm.colorEditor(rgbValue=shadowColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            light = pm.selected()[0].shadowColor.set(color)
        self.setShadowButtonColor(color)
        # self.light.shadowColor.set(color)
        # self.setShadowButtonColor(color)

    def setAiShadowColor(self):
        my_str = self.lights_list[0] + ".aiShadowColor"
        shadowColor = pm.getAttr(my_str)
        # shadowColor = self.light.shadowColor.get()
        color = pm.colorEditor(rgbValue=shadowColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            # light = pm.selected()[0].shadowColor.set(color)
            pm.setAttr(light_name + ".aiShadowColor", color)
        self.setAiShadowButtonColor(color)

    def setColor(self):
        light = self.lights_list[0]
        pm.select(light)
        light = pm.selected()[0]

        shadowColor = light.color.get()
        color = pm.colorEditor(rgbValue=shadowColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)

        # self.light.color.set(color)
        # self.setButtonColor(color)

        for i in self.lights_list:
            light_name = i
            pm.select(i)
            # light = pm.selected()[0].color.set(color)
            light = pm.selected()[0].name()
            pm.setAttr(light + '.color', color)

        self.setButtonColor(color)

    def list_Dif(self, val):
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            # light = pm.selected()[0].emitDiffuse.set(val)
            light = pm.selected()[0].name
            pm.setAttr(light + '.emitDiffuse', val)


    def list_Spe(self, val):
        for i in self.lights_list:
            light_name = i
            pm.select(i)
            # light = pm.selected()[0].emitSpecular.set(val)
            light = pm.selected()[0].name()
            pm.setAttr(light + '.emitSpecular', val)


    def light_ibd(self):
        for i in self.lights_list:
            name = i
            light_instObjGroups = str(name) + '.instObjGroups'
            if cmds.connectionInfo(light_instObjGroups, isSource=True):
                return 1
            else:
                return 0

    def light_ibd_set(self, check):
        for i in self.lights_list:
            # illuminate by default
            print check
            name = i
            dagSetMembers = ''
            light_instObjGroups = str(name) + '.instObjGroups'
            if check:
                cmds.connectAttr(light_instObjGroups, 'defaultLightSet.dagSetMembers', nextAvailable=1, )
            else:
                if cmds.connectionInfo(light_instObjGroups, isSource=True):
                    destinations = cmds.connectionInfo(light_instObjGroups, destinationFromSource=True)
                    for destination in destinations:
                        dagSetMembers = destination
                        print dagSetMembers
                cmds.disconnectAttr(light_instObjGroups, dagSetMembers)
    # ai_lights
    def exposure_set(self, val):
        # print type(val)
        val = float(val)
        for light_name in self.lights_list:
            pm.setAttr(light_name + '.aiExposure', val)

    def sample_set(self, val):
        val = float(val)
        for light_name in self.lights_list:
            pm.setAttr(light_name + '.aiSamples', val)



def showUI(self):
    ui = Lightmanager()
    ui.show()
    return ui

# import light_tool
# reload(light_tool)
ui = showUI('')