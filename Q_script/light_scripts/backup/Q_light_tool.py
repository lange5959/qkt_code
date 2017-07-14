# coding=utf-8

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
        super(Lightmanager, self).__init__()
        self.setWindowTitle('Lighting Manager')

        self.setMinimumWidth(700)
        self.setMinimumHeight(800)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(1200, 100, 250, 150)
        self.setModal(False)


        style_sheet_file = QtCore.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
        style_sheet_file.open(QtCore.QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet_file.readAll()))

        self.buildUI()
        self.populate()

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

        layout = QtWidgets.QGridLayout(self)

        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in sorted(self.lightTypes):
            self.lightTypeCB.addItem(lightType)
        layout.addWidget(self.lightTypeCB, 0, 0)

        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        layout.addWidget(createBtn, 0, 1)

        # scrollWidget
        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 1, 0, 1, 3)

        saveBtn = QtWidgets.QPushButton('save')
        saveBtn.clicked.connect(self.saveLights)
        layout.addWidget(saveBtn, 2, 0)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.importLights)
        layout.addWidget(importBtn, 2, 1)

        refreshBtn = QtWidgets.QPushButton("Refresh")
        refreshBtn.clicked.connect(self.populate)
        layout.addWidget(refreshBtn, 2, 2)

    def saveLights(self):
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
        self.name = QtWidgets.QCheckBox(str(self.light.name()))
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.visibility.set(val))
        layout.addWidget(self.name, 0, 0)
        # solo
        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.solo.emit(val))
        layout.addWidget(soloBtn, 0, 1)
        # del
        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 2)
        # slider
        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        intensity.setMinimum(1.0)
        intensity.setMaximum(10.0)
        intensity.setRange(0.0, 10.0)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        layout.addWidget(intensity, 1, 0, 1, 2)
        # intensity
        intensity = pm.getAttr(self.light.name() + '.intensity')
        intensity = round(intensity, 2)
        self.intensityLin = QtWidgets.QLineEdit(str(intensity))
        self.intensityLin.setMaximumWidth(40)
        self.intensityLin.setMaximumHeight(20)
        self.intensityLin.textChanged .connect(self.intensity)
        layout.addWidget(self.intensityLin, 1, 3)

        # rename
        self.renameLin = QtWidgets.QLineEdit('name')
        self.renameLin.setMaximumWidth(80)
        self.renameLin.setMaximumHeight(20)
        self.renameLin.textChanged.connect(self.renameLight)
        layout.addWidget(self.renameLin, 0, 3, 1, 2)
        # color
        self.colorBtn = QtWidgets.QPushButton('C')
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 1, 2)

        # shadow color
        self.shadowcolorBtn = QtWidgets.QPushButton('Shadow')
        self.shadowcolorBtn.setMaximumWidth(60)
        self.shadowcolorBtn.setMaximumHeight(20)
        self.setShadowButtonColor()
        self.shadowcolorBtn.clicked.connect(self.setShadowColor)
        layout.addWidget(self.shadowcolorBtn, 2, 1)
        # select
        self.selBtn = QtWidgets.QPushButton('#')
        self.selBtn.setCheckable(True)
        self.selBtn.setMaximumWidth(20)
        self.selBtn.setMaximumHeight(20)
        self.selBtn.toggled.connect(self.selectlight)
        # self.selBtn.clicked.connect(self.selectlight)
        layout.addWidget(self.selBtn, 2, 0)
        # emitDiffuse & check
        self.emitDiffuse = QtWidgets.QCheckBox('emitDiffuse')
        self.emitDiffuse.setChecked(self.light.emitDiffuse.get())
        self.emitDiffuse.toggled.connect(lambda val: self.light.emitDiffuse.set(val))
        layout.addWidget(self.emitDiffuse, 1, 4)

        # emitDiffuse & check
        self.emitSpecular = QtWidgets.QCheckBox('emitSpecular')
        self.emitSpecular.setChecked(self.light.emitSpecular.get())
        self.emitSpecular.toggled.connect(lambda val: self.light.emitSpecular.set(val))
        layout.addWidget(self.emitSpecular, 1, 5)
        # Illuminates by default & check
        self.light_connect = QtWidgets.QCheckBox('Illuminates by default')
        self.light_ibd_check = self.light_ibd()
        self.light_connect.setChecked(self.light_ibd_check)
        self.light_connect.toggled.connect(self.light_ibd_set)
        layout.addWidget(self.light_connect, 1, 6)

    def build_ar_UI(self):

        layout = QtWidgets.QGridLayout(self)
        # name & check vis
        self.name = QtWidgets.QCheckBox(str(self.light.name()))
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.visibility.set(val))
        layout.addWidget(self.name, 0, 0)
        # solo
        soloBtn = QtWidgets.QPushButton('Solo')
        soloBtn.setCheckable(True)
        soloBtn.toggled.connect(lambda val: self.solo.emit(val))
        layout.addWidget(soloBtn, 0, 1)
        # del
        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.clicked.connect(self.deleteLight)
        deleteBtn.setMaximumWidth(10)
        layout.addWidget(deleteBtn, 0, 2)
        # slider
        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        intensity.setMinimum(1.0)
        intensity.setMaximum(10.0)
        intensity.setRange(0.0, 10.0)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        layout.addWidget(intensity, 1, 0, 1, 2)
        # int_label
        self.intensity_label = QtWidgets.QLabel('Intensity:')
        layout.addWidget(self.intensity_label, 1, 3)
        # intensity
        ai_intensity =  pm.getAttr(self.light.name()+'.intensity')
        ai_intensity = round(ai_intensity, 2)
        self.intensityLin = QtWidgets.QLineEdit(str(ai_intensity))
        self.intensityLin.setMaximumWidth(60)
        self.intensityLin.setMaximumHeight(20)
        self.intensityLin.textChanged.connect(self.intensity)
        layout.addWidget(self.intensityLin, 1, 4)
        # exp_label
        self.exp_label = QtWidgets.QLabel('Exposure:')
        layout.addWidget(self.exp_label, 2, 3)
        # exp
        ai_exp = pm.getAttr(self.light.name() + '.aiExposure')
        ai_exp = round(ai_exp, 2)
        self.expLin = QtWidgets.QLineEdit(str(ai_exp))
        self.expLin.setMaximumWidth(40)
        self.expLin.setMaximumHeight(20)
        self.expLin.textChanged.connect(self.exposure_set)
        layout.addWidget(self.expLin, 2, 4)

        # sam_label
        self.sam_label = QtWidgets.QLabel('Sample:')
        layout.addWidget(self.sam_label, 2, 5)

        # sample aiSamples
        ai_sample = pm.getAttr(self.light.name() + '.aiSamples')
        ai_sample = round(ai_sample, 2)
        self.samLin = QtWidgets.QLineEdit(str(ai_sample))
        self.samLin.setMaximumWidth(40)
        self.samLin.setMaximumHeight(20)
        self.samLin.textChanged.connect(self.sample_set)
        layout.addWidget(self.samLin, 2, 6)

        # rename
        self.renameLin = QtWidgets.QLineEdit('name')
        self.renameLin.setMaximumWidth(60)
        self.renameLin.setMaximumHeight(20)
        self.renameLin.textChanged.connect(self.renameLight)
        layout.addWidget(self.renameLin, 0, 3, 1, 2)
        # color
        self.colorBtn = QtWidgets.QPushButton('C')
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        self.setButtonColor()
        self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 1, 2)

        # select
        self.selBtn = QtWidgets.QPushButton('AR')
        self.selBtn.setCheckable(True)
        self.selBtn.setMaximumWidth(40)
        self.selBtn.setMaximumHeight(30)
        self.selBtn.toggled.connect(self.selectlight)
        # self.selBtn.clicked.connect(self.selectlight)
        layout.addWidget(self.selBtn, 2, 0)
        # shadow color
        self.ai_shadowcolorBtn = QtWidgets.QPushButton('Shadow')
        self.ai_shadowcolorBtn.setMaximumWidth(60)
        self.ai_shadowcolorBtn.setMaximumHeight(20)
        self.setAiShadowButtonColor()
        self.ai_shadowcolorBtn.clicked.connect(self.setAiShadowColor)
        layout.addWidget(self.ai_shadowcolorBtn, 2, 1)

    def sample_set(self, val):
        val = float(val)
        light = self.light.aiSamples
        light = str(light)
        pm.setAttr(light, val)


    def intensity(self, val):
        val = float(val)
        val = round(val, 2)
        # print val,type(val)
        self.light.intensity.set(val)

    def exposure_set(self, val):
        val = float(val)
        light = self.light.aiExposure
        light = str(light)
        pm.setAttr(light, val)



    def selectlight(self, val):
        if val:
            pm.select(self.light)
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

        self.light.color.set(color)
        self.setButtonColor(color)

    def setShadowColor(self):
        shadowColor = self.light.shadowColor.get()
        color = pm.colorEditor(rgbValue=shadowColor)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)
        self.light.shadowColor.set(color)
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



def showUI(self):
    ui = Lightmanager()
    ui.show()
    return ui

# import light_tool
# reload(light_tool)
ui = showUI('')