# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import sys
import requests

sys.path.append(r'C:\Python27\Lib\site-packages')
class webImg:
    pass


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout)

    from PyQt5.QtGui import QPixmap

    app = QApplication(sys.argv)

    import requests

    url = 'http://192.168.0.34/img/1.jpg'
    req = requests.get(url)

    print(type(req.content))
    print(dir(req))

    photo = QPixmap()
    # photo.loadFromData(req.content, "JPG")
    photo.loadFromData(req.content)

    label = QLabel()
    label.setPixmap(photo)

    widget = QWidget()
    layout = QVBoxLayout()
    widget.setLayout(layout)
    layout.addWidget(label)

    widget.show()

    #####################################################
    sys.exit(app.exec_())