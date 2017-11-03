# coding=utf-8
import bisect
import codecs
from PyQt4.QtCore import *
from PyQt4.QtGui import *

KEY, NODE = range(2)


class BranchNode(object):

    def __init__(self, name, parent=None):
        super(BranchNode, self).__init__(parent)
        self.name = name
        self.parent = parent
        self.children = []

    def orderKey(self):
        return self.name.lower()

    def toString(self):
        return self.name

    def __len__(self):
        return len(self.children)

    def childAtRow(self, row):
        assert 0 <= row < len(self.children)
        return self.children[row][NODE]

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item[NODE] == child:
                return i
        return -1