# coding=utf8
import sys
sys.path.append(r'C:\Users\jack\Documents\maya\2015-x64\scripts')
from Qt import QtCore, QtGui, QtWidgets
#from PySide2 import QtCore
#from PySide2 import QtGui
#from PySide2 import QtWidgets
import glob
import os
import time
import re


class RnameUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RnameUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # QtWidgets.QDialog.__init__(self)

        self.setWindowTitle('Simple UI')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMaximumWidth(500)
        self.setMaximumHeight(900)
        self.dpx = ''

        # self.setModal(True)
        #
        # self.setFixedHeight(800)
        # self.setFixedWidth(800)

        main_lyt = QtWidgets.QVBoxLayout(self)

        path_lyt_a = QtWidgets.QHBoxLayout()
        path_label =  QtWidgets.QLabel('File Path:')
        self.path_lineedit = QtWidgets.QLineEdit('D:\\Temp')
        file_button = QtWidgets.QToolButton()
        file_button.setText("...")
        file_button.defaultAction()

        path_lyt_a.addWidget(path_label)
        path_lyt_a.addWidget(self.path_lineedit)
        path_lyt_a.addWidget(file_button)

        path_lyt_b = QtWidgets.QHBoxLayout()
        self.path_label_b =  QtWidgets.QLabel('New Name:')
        self.new_name_lineedit = QtWidgets.QLineEdit('##_##.001.jpg')

        path_lyt_b.addWidget(self.path_label_b)
        path_lyt_b.addWidget(self.new_name_lineedit)

        list_view_lyt = QtWidgets.QHBoxLayout()  #

        v = QtWidgets.QListView()
        v2 = QtWidgets.QListView()

        self.src_model = QtGui.QStandardItemModel()
        self.tar_model = QtGui.QStandardItemModel()

        list_view_lyt.addWidget(v)
        list_view_lyt.addWidget(v2)
        v.setModel(self.src_model)
        v2.setModel(self.tar_model)

        main_lyt.addLayout(path_lyt_a)
        main_lyt.addLayout(path_lyt_b)
        main_lyt.addLayout(list_view_lyt)

        rename_btn = QtWidgets.QPushButton(text="Rename")
        main_lyt.addWidget(rename_btn)

        rename_btn.clicked.connect(self.reName)
        file_button.clicked.connect(self.openfile)

        self.path_lineedit.textChanged.connect(self.updateSrcList)
        self.new_name_lineedit.textChanged.connect(self.updateTarList)

    def get_suffix(self):
        folder = self.path_lineedit.text()
        file_list = os.listdir(folder)
        suffix = file_list[0].split('.')[-1]
        suffix = '*.'+suffix
        return suffix

    def reName(self):
        folder = self.path_lineedit.text()
        #
        self.dpx = self.get_suffix()

        file_list = glob.glob(folder + '/' + self.dpx)

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
        info_dialog = QtWidgets.QMessageBox()
        info_dialog.setWindowTitle('Done')
        info_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        info_dialog.setText('Done!')
        info_dialog.exec_()

    def openfile(self):
        s = QtWidgets.QFileDialog.getOpenFileName(self, "Open file dialog", "/", "pic files(*.*)")
        print s
        print type(s)
        if s[0] != '':
            print 1
            dir_name_list = map(os.path.dirname, s)
            self.path_lineedit.setText(str(dir_name_list[0]))
        else:
            return

    def updateSrcList(self):
        #
        folder = self.path_lineedit.text()

        self.dpx = self.get_suffix()
        print 'self.dpx', self.dpx
        #
        file_list = glob.glob(folder + '/' + self.dpx)

        base_name_list = map(os.path.basename, file_list)
        item_list = map(QtGui.QStandardItem, base_name_list)

        map(self.src_model.appendRow, item_list)

        self.new_name_lineedit.setText(base_name_list[0])

    def updateTarList(self):
        folder = self.path_lineedit.text()
        file_list = glob.glob(folder + '/' + '*.*')
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
        for f in base_name_list:
            new_name_int = int(new_name[-2])
            new_name_int += n
            new_name_str = str(new_name_int)
            tmp = f.split(".")

            new_name_str = new_name_str.zfill(num)
            new_file = "{0}{3}{1}.{2}".format(new_name_first, new_name_str, new_name[-1], suffix)
            self.tar_model.appendRow(QtGui.QStandardItem(new_file))
            n += 1

# if __name__ == '__main__':
#
#     dialog = RnameUI()
#     dialog.show()
# dialog.exec_()
dialog = RnameUI()
dialog.show()