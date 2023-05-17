# -*- coding: utf-8 -*-
# By：清安无别事
# 公众号：测个der


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1288, 942)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(190, 170, 771, 391))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "输入爬取的链接"))
        self.pushButton.setText(_translate("MainWindow", "爬取"))

import requests
from lxml import etree

class Thread(QThread):
    signal = pyqtSignal(str)
    def __init__(self,url):
        super(Thread, self).__init__()
        self.url = url

    def run(self) -> None:
        html = requests.get(self.url).text
        parse_html = etree.HTML(html)
        selection = parse_html.xpath("//*[@id='js_content']/section")
        for value in selection:
            img_href = value.xpath(
                "//img/@data-src")
            for href in img_href:
                img = requests.get(href).content
                with open('images/' + href[-28:-16] + '.jpg', 'wb') as w:
                    w.write(img)
                    print("加载成功", href)
                self.signal.emit("加载成功~" + href + '\n')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_url)
        self.thread = None

    def get_url(self):
        url = self.ui.lineEdit.text()
        if url:
            self.thread = Thread(url)
            self.thread.signal.connect(self.update_text)
            self.thread.start()
        else:
            self.ui.textEdit.setText("没有链接")

    def update_text(self,text):
        self.ui.textEdit.append(text)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
