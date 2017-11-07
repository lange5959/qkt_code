# coding=utf-8
import bisect
import codecs
from PyQt5.QtCore import (QAbstractItemModel, QModelIndex, QVariant, Qt)

KEY, NODE = range(2)


class BranchNode(object):
    def __init__(self, name, parent=None):
        super(BranchNode, self).__init__()
        self.name = name
        self.parent = parent
        self.children = []

    def __lt__(self, other):
        if isinstance(other, BranchNode):
            return self.orderKey() < other.orderKey()
        return False

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

    def childWithKey(self, key):
        print('*'*5)
        if not self.children:
            print("childWithKey  key","None")
            return None
        print("childWithKey  key", "not None")
        # Causes a -3 deprecation warning. Solution will be to
        # reimplement bisect_left and provide a key function.
        i = bisect.bisect_left(self.children, (key, None))
        # bisect_left 该函数用入处理将会插入重复数值的情况，返回将会插入的位置：
        if i < 0 or i >= len(self.children):
            return None
        if self.children[i][KEY] == key:
            # KEY = 0
            print(self.children, '<<<self.children[i][KEY]')
            return self.children[i][NODE]
        return None

    def insertChild(self, child):
        child.parent = self
        # insort插入操作（自动排序），（name, BranchNode_Object)
        bisect.insort(self.children, (child.orderKey(), child))
        print(self.children, "<<<insertChild", "^^^^^^", "self.name>>>", self.name)

    def hasLeaves(self):
        if not self.children:
            return False
        return isinstance(self.children[0], LeafNode)


class LeafNode(object):
    def __init__(self, fields, parent=None):
        super(LeafNode, self).__init__()
        self.parent = parent
        self.fields = fields

    def orderKey(self):
        return "\t".join(self.fields).lower()

    def toString(self, separator="\t"):
        return separator.join(self.fields)

    def __len__(self):
        return len(self.fields)

    def asRecord(self):
        record = []
        branch = self.parent
        while branch is not None:
            record.insert(0, branch.toString())
            branch = branch.parent
        assert record and not record[0]
        record = record[1:]
        return record + self.fields

    def field(self, column):
        assert 0 <= column <= len(self.fields)
        return self.fields[column]


class TreeOfTableModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(TreeOfTableModel, self).__init__(parent)
        self.columns = 0
        self.root = BranchNode("")
        self.headers = []

    def load(self, filename, nesting, separator):
        self.beginResetModel()
        assert nesting > 0
        self.nesting = nesting
        self.root = BranchNode("")
        # BranchNode??
        exception = None
        fh = None
        try:
            for line in codecs.open(str(filename), "rU", "utf8"):
                if not line:
                    continue
                self.addRecord(line.split(separator), False)
                # addRecord??
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            # self.reset()
            self.endResetModel()
            for i in range(self.columns):
                self.headers.append("Column #{0}".format(i))
            if exception is not None:
                raise exception

    def addRecord(self, fields, callReset=True):
        # fields是一个列表，一整条信息，一行
        # load函数传进来的
        assert len(fields) > self.nesting
        root = self.root
        # root 是一个BranchNode对象
        branch = None
        for i in range(self.nesting):
            key = fields[i].lower()
            # print(key)， key是个字符串，比如国家名字(sheng/city)
            # australia (no state) adelaide
            # country/state/city
            print(key, '<<<')
            branch = root.childWithKey(key)
            if branch is not None:
                root = branch
                print(1, 'root?')
            else:
                print(2, '2?')
                branch = BranchNode(fields[i])  # 第一次循环创建3个branch对象
                # insertChild， children插入操作（自动排序），（name, BranchNode_Object)
                root.insertChild(branch)
                root = branch
                print(root.name, "---root.name")
        print('-'*20)
        assert branch is not None
        items = fields[self.nesting:]
        self.columns = max(self.columns, len(items))
        branch.insertChild(LeafNode(items, branch))
        print('-'*50)
        if callReset:
            self.beginResetModel()
            self.endResetModel()

    def asRecord(self, index):
        leaf = self.nodeFromIndex(index)
        # 返回一个节点
        # 判断返回的节点是不是叶子
        if leaf is not None and isinstance(leaf, LeafNode):
            return leaf.asRecord()  # 必须是叶子节点才行
        return []

    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None or isinstance(node, LeafNode):
            return 0
        return len(node)

    def columnCount(self, parent):
        return self.columns

    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))
        if role != Qt.DisplayRole:
            return QVariant()
        node = self.nodeFromIndex(index)
        assert node is not None
        if isinstance(node, BranchNode):
            return node.toString() if index.column() == 0 else ""
        return node.field(index.column())

    def headerData(self, section, orientation, role):
        if (orientation == Qt.Horizontal and
                    role == Qt.DisplayRole):
            assert 0 <= section <= len(self.headers)
            return self.headers[section]
        return QVariant()

    def index(self, row, column, parent):
        assert self.root
        branch = self.nodeFromIndex(parent)
        assert branch is not None
        return self.createIndex(row, column,
                                branch.childAtRow(row))

    def parent(self, child):
        node = self.nodeFromIndex(child)
        if node is None:
            return QModelIndex()
        parent = node.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != -1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        # internalPointer，返回一个节点的引用
        return (index.internalPointer()
                if index.isValid() else self.root)