# coding=utf-8
from Qt import QtCore, QtGui, QtWidgets
import glob
import os
import time
import re

PATH = r'C:/Users/jack/Pictures/qkt/dog'


class ListView_Icon(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ListView_Icon, self).__init__(parent)

        main_lyt = QtWidgets.QVBoxLayout(self)

        file_button = QtWidgets.QToolButton()
        file_button.setText("...")
        file_button.defaultAction()
        main_lyt.addWidget(file_button)

        self.path_lineedit = QtWidgets.QLineEdit('cat')
        main_lyt.addWidget(self.path_lineedit)

        self.listImage = QtWidgets.QListView()

        main_lyt.addWidget(self.listImage)
        file_button.clicked.connect(self.findImage)
        self.path_lineedit.textChanged.connect(self.updateSrcList)

    def findImage(self, ext='jpg|png|bmp|gif'):
        import os
        image_path = PATH
        allfiles = []
        needExtFilter = (ext != None)
        for root, dirs, files in os.walk(unicode(image_path)):
            for filespath in files:
                filepath = os.path.join(root, filespath)
                # print filepath  路径 path + name
                extension = os.path.splitext(filepath)[1][1:]
                # print extension 后缀名 jpg
                if needExtFilter and extension in ext:
                    allfiles.append(filepath)
                elif not needExtFilter:
                    allfiles.append(filepath)
        model = QtGui.QStandardItemModel(self)
        for pngitem in allfiles:
            name = os.path.basename(unicode(pngitem)).split('.')[0]
            print name, '<<pig_002_mask01'
            path = QtGui.QStandardItem(QtGui.QIcon(unicode(pngitem)), unicode(name))
            print len(allfiles), '<<<<<<'
            #for i in range(len(allfiles)):
            item = QtGui.QStandardItem(path)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            model.appendRow(item)
            self.listImage.setModel(model)
            self.listImage.setIconSize(QtCore.QSize(70, 70))
            self.listImage.setResizeMode(QtWidgets.QListView.Adjust)
            self.listImage.setViewMode(QtWidgets.QListView.IconMode)
            self.listImage.setMovement(QtWidgets.QListView.Static)
            self.listImage.setSpacing(45)
            self.listImage.setWrapping(True)
        return allfiles

    def updateSrcList(self):
        mytext = self.path_lineedit.text()

        model = QtGui.QStandardItemModel(self)


        file_list = glob.glob(PATH + '/' + self.dpx)

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


dog = ListView_Icon()
dog.show()