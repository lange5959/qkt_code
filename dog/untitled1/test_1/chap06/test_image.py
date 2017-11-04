# coding=utf-8

import os
import platform
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import helpform
import newimagedlg
import qrc_resources


__version__ = "1.0.0"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False

        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)

        logDockWidget = QDockWidget("Log", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                      Qt.RightDockWidgetArea)

        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

        self.printer = None

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StylePanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)

        fileNewAction = self.createAction("&New...", self.fileNew,
                                          QKeySequence.New, "filenew", "Create an image file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                                           QKeySequence.Open, "fileopen",
                                           "Open an existing image file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                                           QKeySequence.Save, "filesave", "Save the image")
        fileSaveAsAction = self.createAction("Save &As...",
                                             self.fileSaveAs, icon="filesaveas",
                                             tip="Save the image using a new name")
        filePrintAction = self.createAction("&Print", self.filePrint,
                                            QKeySequence.Print, "fileprint", "Print the image")
        fileQuitAction = self.createAction("&Quit", self.close,
                                           "Ctrl+Q", "filequit", "Close the application")
        editInvertAction = self.createAction("&Invert",
                                             self.editInvert, "Ctrl+I", "editinvert",
                                             "Invert the image's colors", True, "toggled(bool)")
        editSwapRedAndBlueAction = self.createAction(
            "Sw&ap Red and Blue", self.editSwapRedAndBlue,
            "Ctrl+A", "editswap",
            "Swap the image's red and blue color components",
            True, "toggled(bool)")
        editZoomAction = self.createAction("&Zoom...", self.editZoom,
                                           "Alt+Z", "editzoom", "Zoom the image")

        mirrorGroup = QActionGroup(self)

        editUnMirrorAction = self.createAction("&Unmirror",
                                               self.editUnMirror, "Ctrl+U", "editunmirror",
                                               "Unmirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editUnMirrorAction)
        editMirrorHorizontalAction = self.createAction(
            "Mirror &Horizontally", self.editMirrorHorizontal,
            "Ctrl+H", "editmirrorhoriz",
            "Horizontally mirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorHorizontalAction)
        editMirrorVerticalAction = self.createAction(
            "Mirror &Vertically", self.editMirrorVertical,
            "Ctrl+V", "editmirrorvert",
            "Vertically mirror the image", True, "toggled(bool)")
        mirrorGroup.addAction(editMirrorVerticalAction)
        editUnMirrorAction.setChecked(True)
        helpAboutAction = self.createAction("&About Image Changer",
                                            self.helpAbout)
        helpHelpAction = self.createAction("&Help", self.helpHelp,
                                           QKeySequence.HelpContents)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction, fileOpenAction,
                                fileSaveAction, fileSaveAsAction, None,
                                filePrintAction, fileQuitAction)
        self.connect(self.fileMenu, SIGNAL("aboutToShow()"), self.updateFileMenu)

        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editUnMirrorAction, editMirrorHorizontalAction, editMirrorVerticalAction))

        mirrorMenu = editMenu.addMenu(QIcon(":/editmirrot.png"),"&mirror")
        self.addActions(mirrorMenu, (editUnMirrorAction, editMirrorHorizontalAction, editMirrorVerticalAction))

        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShotcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)











