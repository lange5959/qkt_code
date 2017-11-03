# coding=utf-8
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class PenPropertiesDlg(QDialog):
    def __init__(self, parent=None):
        super(PenPropertiesDlg, self).__init__(parent)

        widthLabel = QLabel("&Width:")
        self.widthSpinBox = QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 24)

        self.beveledCheckBox = QCheckBox("&Beveled edges")

        styleLabel = QLabel("&Style")
        self.styleComboBox = QComboBox()
        styleLabel.setBuddy(self.styleComboBox)
        self.styleComboBox.addItems(["Solid", "Dashed", "Dotted",
                                     "DashDotted", "DashDotDotted"])

        okButton = QPushButton("&OK")
        cancelButton = QPushButton("&Cancel")

        buttonLayout = QHBoxLayout()
        # buttonLayout.addStretch(10)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        layout = QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.beveledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2)
        layout.addLayout(buttonLayout, 2, 0, 1, 3)
        self.setLayout(layout)

        self.connect(okButton, SIGNAL("clicked()"),
                     self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"),
                     self, SLOT("reject()"))
        self.setWindowTitle("Pen Properties")


class mainForm(QDialog):
    def __init__(self, parent=None):
        super(mainForm, self).__init__(parent)

        self.width = 1
        self.beveled= False
        self.style = "Solid"

        penButtonInline = QPushButton("Set Pen...(Dumb &inline)")
        penButton = QPushButton("SetPen...(Dumb &class)")
        self.label = QLabel("The Pen has not been set")
        self.label.setTextFormat(Qt.RichText)

        layout = QVBoxLayout()
        layout.addWidget(penButtonInline)
        layout.addWidget(penButton)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.connect(penButtonInline, SIGNAL("clicked()"), self.setPenInline)
        self.connect(penButton, SIGNAL("clicked()"), self.setPenProperties)
        self.setWindowTitle("Pen")
        self.updateData()

    def setPenInline(self):
        pass

    def updateData(self):
        bevel = ''
        if self.beveled:
            bevel = "<br>Beveled"
        self.label.setText("Width = %d<br>Style = %s%s" % (self.width, self.style, bevel))

    def setPenProperties(self):
        dialog = PenPropertiesDlg(self)
        dialog.widthSpinBox.setValue(self.width)
        dialog.beveledCheckBox.setChecked(self.beveled)
        dialog.styleComboBox.setCurrentIndex(dialog.styleComboBox.findText(self.style))
        if dialog.exec_():
            print 1
            self.width = dialog.widthSpinBox.value()
            self.beveled = dialog.beveledCheckBox.isChecked()
            self.style = unicode(dialog.styleComboBox.currentText())
            self.updateData()


app = QApplication(sys.argv)
form = mainForm()
form.show()
app.exec_()










