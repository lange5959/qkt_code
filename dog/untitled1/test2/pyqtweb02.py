import sys
from PyQt4.Qt import *
from PyQt4.QtWebKit import *


class WebView(QWebView):
    def __init__(self):
        super(WebView, self).__init__()
        self.load(QUrl('http://192.168.0.34/picture/index.php/Home/Index/menu'))
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.page().linkClicked.connect(self.linkClicked)
        self.show()

    def linkClicked(self, url):
        print url.toString()
        #self.load(url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    webView = WebView()
    sys.exit(app.exec_())

