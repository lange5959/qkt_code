# coding=utf8
from PySide import QtCore, QtGui
#from PySide2 import QtCore
#from PySide2 import QtGui
#from PySide2 import QtWidgets
import glob
import os
import time
import re


class RnameUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(RnameUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # QtWidgets.QDialog.__init__(self)

        self.setWindowTitle('Simple UI')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # self.setModal(True)
        #
        # self.setFixedHeight(800)
        # self.setFixedWidth(800)

        main_lyt = QtGui.QVBoxLayout(self)

        path_lyt_a = QtGui.QHBoxLayout()
        path_label =  QtGui.QLabel('File Path:')
        self.path_lineedit = QtGui.QLineEdit('path')
        file_button = QtGui.QToolButton()
        file_button.setText("...")
        file_button.defaultAction()

        path_lyt_a.addWidget(path_label)
        path_lyt_a.addWidget(self.path_lineedit)
        path_lyt_a.addWidget(file_button)

        path_lyt_b = QtGui.QHBoxLayout()
        self.path_label_b =  QtGui.QLabel('New Name:')
        self.new_name_lineedit = QtGui.QLineEdit('##_##.001.jpg')

        path_lyt_b.addWidget(self.path_label_b)
        path_lyt_b.addWidget(self.new_name_lineedit)

        list_view_lyt = QtGui.QHBoxLayout()  #

        v = QtGui.QListView()
        v2 = QtGui.QListView()

        self.src_model = QtGui.QStandardItemModel()
        self.tar_model = QtGui.QStandardItemModel()

        list_view_lyt.addWidget(v)
        list_view_lyt.addWidget(v2)
        v.setModel(self.src_model)
        v2.setModel(self.tar_model)

        main_lyt.addLayout(path_lyt_a)
        main_lyt.addLayout(path_lyt_b)
        main_lyt.addLayout(list_view_lyt)

        rename_btn = QtGui.QPushButton(text="Rename")
        main_lyt.addWidget(rename_btn)

        rename_btn.clicked.connect(self.reName)
        file_button.clicked.connect(self.openfile)

        self.path_lineedit.textChanged.connect(self.updateSrcList)
        self.new_name_lineedit.textChanged.connect(self.updateTarList)

    def reName(self):
        folder = self.path_lineedit.text()
        #
        file_list = glob.glob(folder + '/' + '*.dpx')

        this_name = self.new_name_lineedit.text()
        new_name = re.split(r'[_.;,\s]\s*', str(this_name))
        new_name_first = '_'.join(new_name[:-2])
        suffix = re.search('[_.]\d+', str(this_name))
        suffix = suffix.group()
        suffix = re.search('[._]', suffix)
        suffix = suffix.group()

        base_name_list = map(os.path.basename, file_list)
        self.tar_model.clear()
        n = 0
        num = len(new_name[-2])
        os.chdir(folder)
        for f in base_name_list:
            new_name_int = int(new_name[-2])
            new_name_int += n
            new_name_str = str(new_name_int)
            # tmp = f.split(".")

            new_name_str = new_name_str.zfill(num)
            new_file = "{0}{3}{1}.{2}".format(new_name_first, new_name_str, new_name[-1], suffix)
            self.tar_model.appendRow(QtGui.QStandardItem(new_file))
            n += 1
            os.rename(f, new_file)
        info_dialog = QtGui.QMessageBox()
        info_dialog.setWindowTitle('Done')
        info_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        info_dialog.setText('Done!')
        info_dialog.exec_()


    def openfile(self):
        s = QtGui.QFileDialog.getOpenFileName(self, "Open file dialog", "/", "Dpxx files(*.*)")
        dir_name_list = map(os.path.dirname, s)
        self.path_lineedit.setText(str(dir_name_list[0]))

    def updateSrcList(self):
        #
        folder = self.path_lineedit.text()
        #
        file_list = glob.glob(folder + '/' + '*.dpx')

        base_name_list = map(os.path.basename, file_list)
        item_list = map(QtGui.QStandardItem, base_name_list)

        map(self.src_model.appendRow, item_list)

        self.new_name_lineedit.setText(base_name_list[0])

    def updateTarList(self):
        #
        folder = self.path_lineedit.text()
        #
        file_list = glob.glob(folder + '/' + '*.*')
        this_name = self.new_name_lineedit.text()
        # new_name = str(self.new_name_lineedit.text()).split(".")
        new_name = re.split(r'[_.;,\s]\s*', str(this_name))
        new_name_first = '_'.join(new_name[:-2])

        new_name = re.split(r'[_.;,\s]\s*', str(this_name))
        new_name_first = '_'.join(new_name[:-2])
        suffix = re.search('[_.]\d+', str(this_name))
        suffix = suffix.group()
        suffix = re.search('[._]', suffix)
        suffix = suffix.group()

        base_name_list = map(os.path.basename, file_list)
        self.tar_model.clear()
        n = 0
        num = len(new_name[-2])
        for f in base_name_list:
            new_name_int = int(new_name[-2])
            new_name_int += n
            new_name_str = str(new_name_int)
            tmp = f.split(".")

            new_name_str = new_name_str.zfill(num)
            new_file = "{0}{3}{1}.{2}".format(new_name_first, new_name_str, new_name[-1], suffix)
            self.tar_model.appendRow(QtGui.QStandardItem(new_file))
            n += 1

if __name__ == '__main__':

    dialog = RnameUI()
    dialog.show()
# dialog.exec_()

dialog = RnameUI()
dialog.show()