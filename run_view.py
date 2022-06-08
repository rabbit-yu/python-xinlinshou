import os
import sys
import time
from queue import Queue
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from main import HuaWei
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from voice import tips


class tuThread(QThread):
    def __init__(self):
        super(tuThread, self).__init__()

    def get_c(self, q, label_list):
        self.q = q
        self.label_list = label_list

    def run(self):    # 在启动线程后任务从这个函数里面开始执行
        if not os.path.exists('C:/图片'):
            os.mkdir('C:/图片')
        with open(f'C:/图片/已经完成的.txt', 'a') as f:
            with open(f'C:/图片/已经完成的.txt', 'r') as f1:
                r = f1.read()
        con_img_li = r.split('\n')
        while True:
            dir_list = os.listdir('C:/图片')
            if len(dir_list) > 1:
                if self.q.qsize() == 0:
                    for i in self.label_list:
                        i[1].append('下一个')
                        i[0].clear()

                        self.q.put(i)

                for img in dir_list:
                    if 'txt' not in img:
                        if img not in con_img_li:
                            con_img_li.append(img)
                            img_name = os.path.splitext(img)[0]
                            with open(f'C:/图片/已经完成的.txt', 'a') as f:
                                f.write(img + '\n')
                            view = self.q.get()
                            time.sleep(0.5)
                            img_w = QPixmap(f'C:/图片/{img}')
                            time.sleep(0.5)
                            view[0].setPixmap(img_w)
                            view[1].append(img_name)
                            tips()


class mainThread(QThread):    # 建立一个任务线程类
    def __init__(self):
        super(mainThread, self).__init__()

    def get_c(self, text_7, j_time):
        self.text_7 = text_7
        self.j_time = j_time

    def run(self):    # 在启动线程后任务从这个函数里面开始执行
        hw = HuaWei(self.text_7, self.j_time)
        hw.run()


class run_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(run_MainWindow, self).__init__()
        self.tuthread = tuThread()
        self.mainthread = mainThread()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        self.setWindowTitle('监控商品变化')
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1636, 848)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 240, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 480, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 0, 430, 430))
        self.label.setObjectName("label")
        self.text = QtWidgets.QTextEdit(self.centralwidget)
        self.text.setGeometry(QtCore.QRect(200, 435, 430, 50))
        self.label.setObjectName("text")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(700, 0, 430, 430))
        self.label_2.setObjectName("label_2")
        self.text_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_2.setGeometry(QtCore.QRect(700, 435, 430, 50))
        self.label.setObjectName("text_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1240, 0, 430, 430))
        self.label_3.setObjectName("label_3")
        self.text_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_3.setGeometry(QtCore.QRect(1240, 435, 430, 50))
        self.label.setObjectName("text_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 500, 430, 430))
        self.label_4.setObjectName("label_4")
        self.text_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_4.setGeometry(QtCore.QRect(630, 500, 65, 430))
        self.label.setObjectName("text_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(700, 500, 430, 430))
        self.label_5.setObjectName("label_5")
        self.text_5 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_5.setGeometry(QtCore.QRect(1130, 500, 100, 430))
        self.label.setObjectName("text_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1250, 500, 430, 430))
        self.label_6.setObjectName("label_6")
        self.text_6 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_6.setGeometry(QtCore.QRect(1700, 500, 100, 430))
        self.label.setObjectName("text_6")

        self.text_7 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_7.setGeometry(QtCore.QRect(20, 520, 150, 430))
        self.label.setObjectName("text_7")

        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.label_time.setGeometry(QtCore.QRect(20, 50, 121, 51))
        self.label.setObjectName("label_time")

        self.lineEdit_time = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_time.setGeometry(QtCore.QRect(20, 100, 121, 31))
        self.lineEdit_time.setObjectName("lineEdit_time")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1636, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "监视商品上新"))
        self.pushButton.setText(_translate("MainWindow", "开始"))
        self.pushButton_3.setText(_translate("MainWindow", "退出"))
        self.label_time.setText(_translate('MainWindow', '设置间歇时间：'))
        self.label.setText(_translate("MainWindow", "耐心等待"))
        self.label_2.setText(_translate("MainWindow", "耐心等待"))
        self.label_3.setText(_translate("MainWindow", "耐心等待"))
        self.label_4.setText(_translate("MainWindow", "耐心等待"))
        self.label_5.setText(_translate("MainWindow", "耐心等待"))
        self.label_6.setText(_translate("MainWindow", "耐心等待"))
        self.click()
        self.label_list = [
            [self.label, self.text],
            [self.label_2, self.text_2],
            [self.label_3, self.text_3],
            [self.label_4, self.text_4],
            [self.label_5, self.text_5],
            [self.label_6, self.text_6]
        ]
        self.q = Queue()
        for i in self.label_list:
            self.q.put(i)

    def click(self):
        self.pushButton.clicked.connect(self.pen)
        self.pushButton_3.clicked.connect(self.quit)

    @pyqtSlot()
    def quit(self):
        self.tuthread.exit()
        self.mainthread.exit()
        sys.exit(0)

    @pyqtSlot()
    def pen(self):
        self.tuthread.get_c(self.q, self.label_list)
        self.tuthread.start()
        j_time = self.lineEdit_time.text()
        if len(j_time) == 0:
            j_time = 2
        self.mainthread.get_c(self.text_7, int(j_time))
        self.mainthread.start()


