# -*- coding: utf-8 -*-
# title       : QKT_UVMoverMainUI
# description : ''
# author      : MengWei
# date        :
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import sys
import logging

# Third-party modules
from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore
import pymel.core as pm
import maya.cmds as cmds

# Studio modules

# Local modules
import uv_mover

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_UVMoverMainUI_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class UVMoverMainUI(QtGui.QDialog):
    """ Class definition for the custom QComboBox that can select multiple
        options using check-box.
    """

    def __init__(self, parent=None):
        super(UVMoverMainUI, self).__init__(parent)
        self.setFocus()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self._ui.up_btn.clicked.emit()


if __name__ == "__main__":
    import sys

    # app = QtGui.QApplication(sys.argv)
    wgt = UVMoverMainUI()
    wgt.show()
    # app.exec_()