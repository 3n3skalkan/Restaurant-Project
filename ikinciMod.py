from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import random

class IkinciModPencere(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setStyleSheet("background-color: darkgray")
        Form.resize(800, 600)


        self.sabitAkis = QtWidgets.QFrame(Form)
        self.sabitAkis.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.sabitAkis.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sabitAkis.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sabitAkis.setStyleSheet("background-color: rgb(54, 69, 79);  color: white")
        self.sabitAkis.setObjectName("sabitAkis")
        self.sabitAkis.setVisible(False)
        
        self.hesaplama = QtWidgets.QPushButton(self.sabitAkis)
        self.hesaplama.setGeometry(QtCore.QRect(300, 380, 150, 40))
        self.hesaplama.clicked.connect(self.hesaplaMethod)
        self.hesaplama.setStyleSheet("background-color: rgb(32,32,32)")
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.hesaplama.setFont(font)
        self.hesaplama.setObjectName("hesaplama")

        self.musteriSureText = QtWidgets.QLabel(self.sabitAkis)
        self.musteriSureText.setGeometry(QtCore.QRect(200, 310, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        self.musteriSureText.setFont(font)
        self.musteriSureText.setObjectName("musteriSureText")

        self.musteriSayiText = QtWidgets.QLabel(self.sabitAkis)
        self.musteriSayiText.setGeometry(QtCore.QRect(200, 230, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        self.musteriSayiText.setFont(font)
        self.musteriSayiText.setObjectName("musteriSayiText")

        self.toplamSureField = QtWidgets.QLineEdit(self.sabitAkis)
        self.toplamSureField.setGeometry(QtCore.QRect(350, 150, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        self.toplamSureField.setFont(font)
        self.toplamSureField.setObjectName("toplamSureField")

        self.musteriSayiField = QtWidgets.QLineEdit(self.sabitAkis)
        self.musteriSayiField.setGeometry(QtCore.QRect(350, 230, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        self.musteriSayiField.setFont(font)
        self.musteriSayiField.setObjectName("musteriSayiField")

        self.toplamSure = QtWidgets.QLabel(self.sabitAkis)
        self.toplamSure.setGeometry(QtCore.QRect(250, 150, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        self.toplamSure.setFont(font)
        self.toplamSure.setObjectName("toplamSure")

        self.musteriSureField = QtWidgets.QLineEdit(self.sabitAkis)
        self.musteriSureField.setGeometry(QtCore.QRect(350, 310, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        self.musteriSureField.setFont(font)
        self.musteriSureField.setObjectName("musteriSureField")


        self.sabitAkisButton = QtWidgets.QPushButton(Form)
        self.sabitAkisButton.setGeometry(QtCore.QRect(325, 200, 150, 40))
        self.sabitAkisButton.clicked.connect(self.sabitAkisMethod)
        self.sabitAkisButton.setStyleSheet("background-color: rgb(32,32,32); color: white")
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setBold(True)
        font.setWeight(75)
        self.sabitAkisButton.setFont(font)
        self.sabitAkisButton.setObjectName("sabitAkisButton")

        self.rastgeleAkisButton = QtWidgets.QPushButton(Form)
        self.rastgeleAkisButton.setGeometry(QtCore.QRect(325, 300, 150, 40))
        self.rastgeleAkisButton.clicked.connect(self.rastgeleAkisMethod)
        self.rastgeleAkisButton.setStyleSheet("background-color: rgb(32,32,32); color: white")
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setBold(True)
        font.setWeight(75)
        self.rastgeleAkisButton.setFont(font)
        self.rastgeleAkisButton.setObjectName("rastgeleAkisButton")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def sabitAkisMethod(self):
        self.sabitAkis.setVisible(True)
        self.sabitAkisButton.setVisible(False)
        self.rastgeleAkisButton.setVisible(False)

    def hesaplaMethod(self):
        try:
            toplamSure = int(self.toplamSureField.text())
            musteriSayi = int(self.musteriSayiField.text())
            musteriSure = int(self.musteriSureField.text())


            self.masa = 1
            self.garson = 1
            self.asci = 1

            toplamMusteri = (toplamSure / musteriSure) * musteriSayi
            ayrilanMusteri = toplamSure / 20

            netMusteriSay = toplamMusteri - ayrilanMusteri
            toplamKazanc = netMusteriSay - (self.masa + self.garson + self.asci)

            gecici = 0.0
            guncelKazanc = []

            while True:
                ayrilanMusteri -= (self.masa + self.garson + 2 * self.asci) / 9
                netMusteriSay = toplamMusteri - ayrilanMusteri
                gecici = netMusteriSay - (self.masa + self.garson + self.asci)
                guncelKazanc.append(gecici)

                if len(guncelKazanc) >= 2 and guncelKazanc[-1] < guncelKazanc[-2]:
                    QMessageBox.information(self.sabitAkis, 'En iyi senaryo', "En iyi kazanç şartları: {} Masa, {} Garson, {} Aşçı\n\nMaksimum kazanç değeri: {}".format(self.masa, self.garson, self.asci, guncelKazanc[-2]))
                    break

                self.asci += 1

                if len(guncelKazanc) >= 2 and guncelKazanc[-1] < guncelKazanc[-2]:
                    break

                self.garson += 1

                if len(guncelKazanc) >= 2 and guncelKazanc[-1] < guncelKazanc[-2]:
                    break

                self.masa += random.randint(6, 9)
        except Exception as e:
            print("Hata:", e)

    def rastgeleAkisMethod(self):
        self.sabitAkis.setVisible(True)
        self.musteriSayiField.setReadOnly(True)
        self.musteriSayiField.setText(str(random.randint(1,20)))
        self.musteriSureField.setReadOnly(True)
        self.musteriSureField.setText(str(random.randint(1,20)))
        self.sabitAkisButton.setVisible(False)
        self.rastgeleAkisButton.setVisible(False)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "2. Mod"))
        self.hesaplama.setText(_translate("Form", "Hesapla"))
        self.musteriSureText.setText(_translate("Form", "Müşteri Gelme Sıklığı:"))
        self.musteriSayiText.setText(_translate("Form", "Gelen Müşteri Sayısı:"))
        self.toplamSure.setText(_translate("Form", "Toplam Süre:"))
        self.sabitAkisButton.setText(_translate("Form", "Sabit Akış Modeli"))
        self.rastgeleAkisButton.setText(_translate("Form", "Rastgele Akış Modeli"))
