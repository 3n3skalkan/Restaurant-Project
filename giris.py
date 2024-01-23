from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from birinciMod import BirinciModPencere
from ikinciMod import IkinciModPencere


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1200, 800)
        MainWindow.setStyleSheet("background-color: rgb(54, 69, 79)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        screen_geometry = QtWidgets.QDesktopWidget().availableGeometry()
        MainWindow.setGeometry(
            (screen_geometry.width() - MainWindow.width()) // 2,
            (screen_geometry.height() - MainWindow.height()) // 2,
            MainWindow.width(),
            MainWindow.height()
        )


        self.birinciMod = QtWidgets.QPushButton(self.centralwidget)
        self.birinciMod.setStyleSheet("background-color: rgb(32,32,32); color: white")
        self.birinciMod.setGeometry(QtCore.QRect(550, 300, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.birinciMod.setFont(font)
        self.birinciMod.setObjectName("birinciMod")


        self.ikinciMod = QtWidgets.QPushButton(self.centralwidget)
        self.ikinciMod.setStyleSheet("background-color: rgb(32,32,32); color: white")
        self.ikinciMod.setGeometry(QtCore.QRect(550, 380, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ikinciMod.setFont(font)
        self.ikinciMod.setObjectName("ikinciMod")


        self.giristext = QtWidgets.QLabel(self.centralwidget)
        self.giristext.setStyleSheet("color: white")
        self.giristext.setGeometry(QtCore.QRect(365, 170, 470, 80))
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.giristext.setFont(font)
        self.giristext.setObjectName("giristext")


        self.cikis = QtWidgets.QPushButton(self.centralwidget)
        self.cikis.setStyleSheet("background-color: rgb(32,32,32); color: white")
        self.cikis.setGeometry(QtCore.QRect(550, 460, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.cikis.setFont(font)
        self.cikis.setObjectName("cikis")
        self.cikis.clicked.connect(sys.exit)

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.birinciMod.clicked.connect(self.showBirinciModFrame)
        self.ikinciMod.clicked.connect(self.showIkinciModFrame)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ana Menü"))
        self.birinciMod.setText(_translate("MainWindow", "1. mod"))
        self.ikinciMod.setText(_translate("MainWindow", "2. mod"))
        self.giristext.setText(_translate("MainWindow", "Restoran Simulator"))
        self.cikis.setText(_translate("MainWindow", "Çıkış"))

    def showBirinciModFrame(self):
        self.FormBir = QtWidgets.QWidget()
        self.uiBir = BirinciModPencere()
        self.uiBir.setupUi(self.FormBir)
        self.FormBir.show()

    def showIkinciModFrame(self):
        self.FormIki = QtWidgets.QWidget()
        self.uiIki = IkinciModPencere()
        self.uiIki.setupUi(self.FormIki)
        self.FormIki.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())