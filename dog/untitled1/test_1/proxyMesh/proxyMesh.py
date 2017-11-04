import sys
sys.path.append('E:/RND/proxyMesh/')
from PySide import QtCore, QtGui
import maya.OpenMayaUI as omUI
import maya.cmds as mc
import maya.mel as mm
import Images
import shiboken

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 530)
        MainWindow.setMinimumSize(QtCore.QSize(320, 530))
        MainWindow.setMaximumSize(QtCore.QSize(320, 530))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.voxelSizeLabel = QtGui.QLabel(self.centralwidget)
        self.voxelSizeLabel.setGeometry(QtCore.QRect(10, 240, 90, 20))
        self.voxelSizeLabel.setObjectName("voxelSizeLabel")
        self.voxelSizeSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.voxelSizeSpinBox.setGeometry(QtCore.QRect(100, 238, 62, 25))
        self.voxelSizeSpinBox.setDecimals(3)
        self.voxelSizeSpinBox.setMinimum(0.001)
        self.voxelSizeSpinBox.setProperty("value", 1.0)
        self.voxelSizeSpinBox.setObjectName("voxelSizeSpinBox")
        self.meshLabel = QtGui.QLabel(self.centralwidget)
        self.meshLabel.setGeometry(QtCore.QRect(10, 140, 40, 15))
        self.meshLabel.setMinimumSize(QtCore.QSize(40, 15))
        self.meshLabel.setMaximumSize(QtCore.QSize(40, 15))
        self.meshLabel.setObjectName("meshLabel")
        self.meshLineEdit = QtGui.QLineEdit(self.centralwidget)
        self.meshLineEdit.setGeometry(QtCore.QRect(50, 135, 210, 25))
        self.meshLineEdit.setMinimumSize(QtCore.QSize(210, 25))
        self.meshLineEdit.setMaximumSize(QtCore.QSize(210, 25))
        self.meshLineEdit.setObjectName("meshLineEdit")
        self.meshLoadBtn = QtGui.QPushButton(self.centralwidget)
        self.meshLoadBtn.setGeometry(QtCore.QRect(270, 135, 40, 25))
        self.meshLoadBtn.setMinimumSize(QtCore.QSize(40, 25))
        self.meshLoadBtn.setMaximumSize(QtCore.QSize(40, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.meshLoadBtn.setFont(font)
        self.meshLoadBtn.setObjectName("meshLoadBtn")
        self.createBtn = QtGui.QPushButton(self.centralwidget)
        self.createBtn.setGeometry(QtCore.QRect(100, 170, 120, 25))
        self.createBtn.setMinimumSize(QtCore.QSize(120, 25))
        self.createBtn.setMaximumSize(QtCore.QSize(120, 25))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.createBtn.setFont(font)
        self.createBtn.setObjectName("createBtn")
        self.headerLabel = QtGui.QLabel(self.centralwidget)
        self.headerLabel.setGeometry(QtCore.QRect(0, 0, 320, 100))
        self.headerLabel.setMinimumSize(QtCore.QSize(320, 100))
        self.headerLabel.setMaximumSize(QtCore.QSize(320, 100))
        self.headerLabel.setText("")
        self.headerLabel.setPixmap(QtGui.QPixmap(":/Images/proxyGeometry.jpg"))
        self.headerLabel.setObjectName("headerLabel")
        self.createLabel = QtGui.QLabel(self.centralwidget)
        self.createLabel.setGeometry(QtCore.QRect(0, 110, 320, 15))
        self.createLabel.setMinimumSize(QtCore.QSize(320, 15))
        self.createLabel.setMaximumSize(QtCore.QSize(320, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.createLabel.setFont(font)
        self.createLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.createLabel.setObjectName("createLabel")
        self.modifyLabel = QtGui.QLabel(self.centralwidget)
        self.modifyLabel.setGeometry(QtCore.QRect(0, 210, 320, 15))
        self.modifyLabel.setMinimumSize(QtCore.QSize(320, 15))
        self.modifyLabel.setMaximumSize(QtCore.QSize(320, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.modifyLabel.setFont(font)
        self.modifyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.modifyLabel.setObjectName("modifyLabel")
        self.bakeProxyLabel = QtGui.QLabel(self.centralwidget)
        self.bakeProxyLabel.setGeometry(QtCore.QRect(0, 380, 320, 15))
        self.bakeProxyLabel.setMinimumSize(QtCore.QSize(320, 15))
        self.bakeProxyLabel.setMaximumSize(QtCore.QSize(320, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.bakeProxyLabel.setFont(font)
        self.bakeProxyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bakeProxyLabel.setObjectName("bakeProxyLabel")
        self.bakeProxyBtn = QtGui.QPushButton(self.centralwidget)
        self.bakeProxyBtn.setGeometry(QtCore.QRect(100, 440, 120, 25))
        self.bakeProxyBtn.setObjectName("bakeProxyBtn")
        self.voxelSizeBtn = QtGui.QPushButton(self.centralwidget)
        self.voxelSizeBtn.setGeometry(QtCore.QRect(170, 238, 40, 25))
        self.voxelSizeBtn.setObjectName("voxelSizeBtn")
        self.bakeStepSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.bakeStepSpinBox.setGeometry(QtCore.QRect(80, 403, 62, 25))
        self.bakeStepSpinBox.setMinimum(0.01)
        self.bakeStepSpinBox.setProperty("value", 1.0)
        self.bakeStepSpinBox.setObjectName("bakeStepSpinBox")
        self.bakeStepLabel = QtGui.QLabel(self.centralwidget)
        self.bakeStepLabel.setGeometry(QtCore.QRect(10, 405, 90, 20))
        self.bakeStepLabel.setObjectName("bakeStepLabel")
        self.loadProxyLabel = QtGui.QLabel(self.centralwidget)
        self.loadProxyLabel.setGeometry(QtCore.QRect(0, 475, 320, 15))
        self.loadProxyLabel.setMinimumSize(QtCore.QSize(320, 15))
        self.loadProxyLabel.setMaximumSize(QtCore.QSize(320, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.loadProxyLabel.setFont(font)
        self.loadProxyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loadProxyLabel.setObjectName("loadProxyLabel")
        self.loadProxyBtn = QtGui.QPushButton(self.centralwidget)
        self.loadProxyBtn.setGeometry(QtCore.QRect(100, 500, 120, 25))
        self.loadProxyBtn.setObjectName("loadProxyBtn")
        self.isoValueBtn = QtGui.QPushButton(self.centralwidget)
        self.isoValueBtn.setGeometry(QtCore.QRect(170, 270, 40, 25))
        self.isoValueBtn.setObjectName("isoValueBtn")
        self.isoValueLabel = QtGui.QLabel(self.centralwidget)
        self.isoValueLabel.setGeometry(QtCore.QRect(10, 272, 90, 20))
        self.isoValueLabel.setObjectName("isoValueLabel")
        self.isoValueSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.isoValueSpinBox.setGeometry(QtCore.QRect(100, 270, 62, 25))
        self.isoValueSpinBox.setDecimals(3)
        self.isoValueSpinBox.setMinimum(-100.0)
        self.isoValueSpinBox.setMaximum(100.0)
        self.isoValueSpinBox.setSingleStep(0.01)
        self.isoValueSpinBox.setProperty("value", 0.0)
        self.isoValueSpinBox.setObjectName("isoValueSpinBox")
        self.adaptivityBtn = QtGui.QPushButton(self.centralwidget)
        self.adaptivityBtn.setGeometry(QtCore.QRect(170, 305, 40, 25))
        self.adaptivityBtn.setObjectName("adaptivityBtn")
        self.adaptivitySpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.adaptivitySpinBox.setGeometry(QtCore.QRect(100, 305, 62, 25))
        self.adaptivitySpinBox.setDecimals(3)
        self.adaptivitySpinBox.setMinimum(0.0)
        self.adaptivitySpinBox.setMaximum(2.0)
        self.adaptivitySpinBox.setSingleStep(0.01)
        self.adaptivitySpinBox.setProperty("value", 0.0)
        self.adaptivitySpinBox.setObjectName("adaptivitySpinBox")
        self.adaptivityLabel = QtGui.QLabel(self.centralwidget)
        self.adaptivityLabel.setGeometry(QtCore.QRect(10, 305, 90, 20))
        self.adaptivityLabel.setObjectName("adaptivityLabel")
        self.edgeToleranceBtn = QtGui.QPushButton(self.centralwidget)
        self.edgeToleranceBtn.setGeometry(QtCore.QRect(170, 340, 40, 25))
        self.edgeToleranceBtn.setObjectName("edgeToleranceBtn")
        self.edgeToleranceLabel = QtGui.QLabel(self.centralwidget)
        self.edgeToleranceLabel.setGeometry(QtCore.QRect(10, 340, 90, 20))
        self.edgeToleranceLabel.setObjectName("edgeToleranceLabel")
        self.edgeToleranceSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.edgeToleranceSpinBox.setGeometry(QtCore.QRect(100, 340, 62, 25))
        self.edgeToleranceSpinBox.setDecimals(3)
        self.edgeToleranceSpinBox.setMinimum(0.0)
        self.edgeToleranceSpinBox.setMaximum(1.0)
        self.edgeToleranceSpinBox.setSingleStep(0.01)
        self.edgeToleranceSpinBox.setProperty("value", 0.5)
        self.edgeToleranceSpinBox.setObjectName("edgeToleranceSpinBox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Proxy Geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.voxelSizeLabel.setText(QtGui.QApplication.translate("MainWindow", "voxelSize:-", None, QtGui.QApplication.UnicodeUTF8))
        self.meshLabel.setText(QtGui.QApplication.translate("MainWindow", "Mesh:-", None, QtGui.QApplication.UnicodeUTF8))
        self.meshLoadBtn.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.createBtn.setText(QtGui.QApplication.translate("MainWindow", "Make Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.createLabel.setText(QtGui.QApplication.translate("MainWindow", "Create Proxy :-----------------------------------", None, QtGui.QApplication.UnicodeUTF8))
        self.modifyLabel.setText(QtGui.QApplication.translate("MainWindow", "Modify Proxy Output :---------------------------", None, QtGui.QApplication.UnicodeUTF8))
        self.bakeProxyLabel.setText(QtGui.QApplication.translate("MainWindow", "Bake Proxy :-------------------------------------", None, QtGui.QApplication.UnicodeUTF8))
        self.bakeProxyBtn.setText(QtGui.QApplication.translate("MainWindow", "Bake Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.voxelSizeBtn.setText(QtGui.QApplication.translate("MainWindow", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.bakeStepLabel.setText(QtGui.QApplication.translate("MainWindow", "Step Frame:-", None, QtGui.QApplication.UnicodeUTF8))
        self.loadProxyLabel.setText(QtGui.QApplication.translate("MainWindow", "Load Proxy :-------------------------------------", None, QtGui.QApplication.UnicodeUTF8))
        self.loadProxyBtn.setText(QtGui.QApplication.translate("MainWindow", "Load Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.isoValueBtn.setText(QtGui.QApplication.translate("MainWindow", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.isoValueLabel.setText(QtGui.QApplication.translate("MainWindow", "isoValue:-", None, QtGui.QApplication.UnicodeUTF8))
        self.adaptivityBtn.setText(QtGui.QApplication.translate("MainWindow", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.adaptivityLabel.setText(QtGui.QApplication.translate("MainWindow", "adaptivity:-", None, QtGui.QApplication.UnicodeUTF8))
        self.edgeToleranceBtn.setText(QtGui.QApplication.translate("MainWindow", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.edgeToleranceLabel.setText(QtGui.QApplication.translate("MainWindow", "edgeTolerance:-", None, QtGui.QApplication.UnicodeUTF8))
        self.meshLoadBtn.clicked.connect(self.loadMeshFn)
        self.createBtn.clicked.connect(self.createProxyFn)
        self.bakeProxyBtn.clicked.connect(self.bakeGeoFn)
        self.loadProxyBtn.clicked.connect(self.importGeoFn)
        self.voxelSizeBtn.clicked.connect(self.setVoxelSizeFn)
        self.isoValueBtn.clicked.connect(self.setIsoValueFn)
        self.adaptivityBtn.clicked.connect(self.setAdaptivityFn)
        self.edgeToleranceBtn.clicked.connect(self.setEdgeToleranceFn)

def getMayaWindow():
    ptr = omUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)

class proxyMeshUI(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setupUi(self)

    def loadMeshFn(self):
        userSel = mc.ls(sl=True)
        userSelShape = mc.listRelatives(userSel[0], s=True)
        if mc.nodeType(userSelShape[0]) != 'mesh':
            print 'Select PolyMesh Only'
        else:
            #return userSelShape[0]
            self.meshLineEdit.setText(userSelShape[0])

    def createProxyFn(self):
        mc.loadPlugin('OpenVDB')
        #Nodes
        sourceMesh = str(self.meshLineEdit.text())
        vdbFromPolyNode = mc.createNode ('BE_VDBFromPolygons', n='polyToVDB#')
        vdbConvertNode = mc.createNode ('BE_VDBConvertVDB', n='vdbToPoly#')
        outMesh = mc.createNode('mesh', n='vdbProxyMeshShape#')
        #Connect Nodes
        mc.connectAttr((sourceMesh+'.worldMesh[0]'), (vdbFromPolyNode+'.MeshInput'), f=True)
        mc.connectAttr((sourceMesh+'.worldMesh[0]'), (vdbConvertNode+'.RefMeshInput'), f=True)
        mc.connectAttr((vdbFromPolyNode+'.VdbOutput'), (vdbConvertNode+'.vdbInput'), f=True)
        mc.connectAttr((vdbConvertNode+'.meshOutput[0]'), (outMesh+'.inMesh'), f=True)
        #Set Initial Attribute
        mc.setAttr((vdbConvertNode+'.ConvertTo'), 1)
        mc.setAttr((vdbConvertNode+'.InvertNormal'), 1)
        mc.setAttr((vdbConvertNode+'.UseRefmesh'), 1)
        mc.setAttr((vdbConvertNode+'.SharpenFeatures'), 1)
        mc.select(cl=True)
        mc.select(outMesh)
        mc.sets(e=True, forceElement='initialShadingGroup')

    def setVoxelSizeFn(self):
        proxyMesh = mc.ls(sl=True)
        proxyMeshShape = mc.listRelatives(proxyMesh[0], s=True)
        vdbConvertNode = mc.listConnections((proxyMeshShape[0]+'.inMesh'), destination=True)
        vdbFromPolyNode = mc.listConnections((vdbConvertNode[0]+'.vdbInput'), destination=True)
        voxelSize = self.voxelSizeSpinBox.value()
        mc.setAttr((vdbFromPolyNode[0]+'.VoxelSize'), voxelSize )

    def setIsoValueFn(self):
        proxyMesh = mc.ls(sl=True)
        proxyMeshShape = mc.listRelatives(proxyMesh[0], s=True)
        vdbConvertNode = mc.listConnections((proxyMeshShape[0]+'.inMesh'), destination=True)
        isoValue = self.isoValueSpinBox.value()
        mc.setAttr((vdbConvertNode[0]+'.isovalue'), isoValue )

    def setAdaptivityFn(self):
        proxyMesh = mc.ls(sl=True)
        proxyMeshShape = mc.listRelatives(proxyMesh[0], s=True)
        vdbConvertNode = mc.listConnections((proxyMeshShape[0]+'.inMesh'), destination=True)
        adaptivity = self.adaptivitySpinBox.value()
        mc.setAttr((vdbConvertNode[0]+'.adaptivity'), adaptivity )

    def setEdgeToleranceFn(self):
        proxyMesh = mc.ls(sl=True)
        proxyMeshShape = mc.listRelatives(proxyMesh[0], s=True)
        vdbConvertNode = mc.listConnections((proxyMeshShape[0]+'.inMesh'), destination=True)
        edgeTolerance = self.edgeToleranceSpinBox.value()
        mc.setAttr((vdbConvertNode[0]+'.EdgeTolerance'), edgeTolerance )

    def bakeGeoFn(self):
        mc.loadPlugin('AbcExport')
        proxyObj = mc.ls(sl=True)
        stepFrame = self.bakeStepSpinBox.value()
        startFrame = int(mc.playbackOptions(min=True, q=True))
        endFrame = int(mc.playbackOptions(max=True, q=True))
        baseDir = mc.workspace(q=True, rd=True)
        cacheDir = (baseDir + 'cache')
        jobArg = ('-root ' + proxyObj[0] + ' -uvWrite -writeVisibility -frs 1.0 -frameRange ' + str(startFrame) +' ' + str(endFrame) +' -step '+ str(stepFrame) + ' -file \"'+ cacheDir +'/'+ proxyObj[0] +'.abc\"')
        mc.AbcExport(v=True, j=jobArg)
        
    def importGeoFn(self):
        mc.loadPlugin('AbcImport')
        filename = mc.fileDialog2(fileMode=1, caption="Import Alembic")
        mc.AbcImport(filename[0], mode='import')