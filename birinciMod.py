from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import threading, random , time, queue

class Semaphore:
    def __init__(self, initial):
        self.signal_count = initial
        self.condition = threading.Condition() 

    def wait(self):
        with self.condition: 
            while self.signal_count <= 0:
                self.condition.wait()
            self.signal_count -= 1

    def signal(self):
        with self.condition:
            self.signal_count += 1 
            self.condition.notify()

txtDosya = "path txt file"

musteriOncelik = queue.PriorityQueue() #gelen müşterileri ilk olarak bu kuyruk içerisine atacağız ardından öncelik değerine göre sırasıyla alacağız
garsonSiparisSira = queue.Queue() #bu kuyruk garsonların sipariş alacağı masaları bir kuyruğa koyar ve buradan sırasıyla her thread bir tane işlemi yapar
asciYemekHazirlama = queue.Queue()
kasiyerOdemeAlma = queue.Queue()

oncelikliSira = []
garsonSira = []
asciSira = []
i = 0
girisYapanMusteri = 0
garsonSay = 0
musteriThreads = []
kasiyerCikisBayragi = False #True olduğunda program çıkış yapar

masaMultiplex = Semaphore(0)

masaMutexList = [Semaphore(1) for _ in range(6)]
masaSiparisDurumList = [Semaphore(1) for _ in range(6)]

garsonMutex = Semaphore(0)
garsonSiparisDurumuMutex = Semaphore(1)

asciMutex = Semaphore(0)
asciYemekSay = 2

kasiyerMutex = Semaphore(0)

class BirinciModPencere(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setStyleSheet("background-color: darkgray")
        Form.resize(1400, 800)


        self.musteriFrame = QtWidgets.QFrame(Form)
        self.musteriFrame.setStyleSheet("background-color: rgb(54, 69, 79); color: white")
        self.musteriFrame.setGeometry(QtCore.QRect(250, 15, 750, 770))
        self.musteriFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.musteriFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.musteriFrame.setObjectName("musteriFrame")

        self.masa1 = QtWidgets.QPushButton(self.musteriFrame)
        self.masa1.setEnabled(False)
        self.masa1.setGeometry(QtCore.QRect(100, 100, 200, 125))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.masa1.setFont(font)
        self.masa1.setObjectName("masa1")

        self.masa2 = QtWidgets.QPushButton(self.musteriFrame)
        self.masa2.setEnabled(False)
        self.masa2.setGeometry(QtCore.QRect(450, 100, 200, 125))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.masa2.setFont(font)
        self.masa2.setObjectName("masa2")

        self.masa3 = QtWidgets.QPushButton(self.musteriFrame)
        self.masa3.setEnabled(False)
        self.masa3.setGeometry(QtCore.QRect(100, 300, 200, 125))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.masa3.setFont(font)
        self.masa3.setObjectName("masa3")

        self.masa4 = QtWidgets.QPushButton(self.musteriFrame)
        self.masa4.setEnabled(False)
        self.masa4.setGeometry(QtCore.QRect(450, 300, 200, 125))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.masa4.setFont(font)
        self.masa4.setObjectName("masa4")

        self.masa5 = QtWidgets.QPushButton(self.musteriFrame)
        self.masa5.setEnabled(False)
        self.masa5.setGeometry(QtCore.QRect(100, 500, 200, 125))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.masa5.setFont(font)
        self.masa5.setObjectName("masa5")

        self.masa6 = QtWidgets.QPushButton(self.musteriFrame)
        self.masa6.setEnabled(False)
        self.masa6.setGeometry(QtCore.QRect(450, 500, 200, 125))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.masa6.setFont(font)
        self.masa6.setObjectName("masa6")


        self.garsonFrame = QtWidgets.QFrame(Form)
        self.garsonFrame.setStyleSheet("background-color: rgb(54, 69, 79); color: white")
        self.garsonFrame.setGeometry(QtCore.QRect(1015, 15, 370, 470))
        self.garsonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.garsonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.garsonFrame.setObjectName("garsonFrame")

        self.garson1 = QtWidgets.QPushButton(self.garsonFrame)
        self.garson1.setEnabled(False)
        self.garson1.setGeometry(QtCore.QRect(80, 50, 210, 100))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.garson1.setFont(font)
        self.garson1.setObjectName("garson1")

        self.garson2 = QtWidgets.QPushButton(self.garsonFrame)
        self.garson2.setEnabled(False)
        self.garson2.setGeometry(QtCore.QRect(80, 185, 210, 100))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.garson2.setFont(font)
        self.garson2.setObjectName("garson2")

        self.garson3 = QtWidgets.QPushButton(self.garsonFrame)
        self.garson3.setEnabled(False)
        self.garson3.setGeometry(QtCore.QRect(80, 320, 210, 100))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.garson3.setFont(font)
        self.garson3.setObjectName("garson3")


        self.asciFrame = QtWidgets.QFrame(Form)
        self.asciFrame.setStyleSheet("background-color: rgb(54, 69, 79); color: white")
        self.asciFrame.setGeometry(QtCore.QRect(1015, 500, 370, 285))
        self.asciFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.asciFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.asciFrame.setObjectName("asciFrame")

        self.asci1 = QtWidgets.QPushButton(self.asciFrame)
        self.asci1.setEnabled(False)
        self.asci1.setGeometry(QtCore.QRect(80, 30, 210, 100))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.asci1.setFont(font)
        self.asci1.setObjectName("asci1")

        self.asci2 = QtWidgets.QPushButton(self.asciFrame)
        self.asci2.setEnabled(False)
        self.asci2.setGeometry(QtCore.QRect(80, 160, 210, 100))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.asci2.setFont(font)
        self.asci2.setObjectName("asci2")


        self.kasiyerFrame = QtWidgets.QFrame(Form)
        self.kasiyerFrame.setStyleSheet("background-color: rgb(54, 69, 79); color: white")
        self.kasiyerFrame.setGeometry(QtCore.QRect(15, 15, 220, 220))
        self.kasiyerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.kasiyerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.kasiyerFrame.setObjectName("kasiyerFrame")

        self.kasiyerText = QtWidgets.QLabel(self.kasiyerFrame)
        self.kasiyerText.setStyleSheet("color: white")
        self.kasiyerText.setGeometry(QtCore.QRect(80, 20, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.kasiyerText.setFont(font)
        self.kasiyerText.setObjectName("kasiyerText")

        self.kasiyerCikti = QtWidgets.QTextEdit(self.kasiyerFrame)
        self.kasiyerCikti.setStyleSheet("color: white")
        self.kasiyerCikti.setEnabled(False)
        self.kasiyerCikti.setGeometry(QtCore.QRect(20, 45, 180, 160))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        self.kasiyerCikti.setFont(font)
        self.kasiyerCikti.setObjectName("kasiyerCikti")


        self.buttonFrame = QtWidgets.QFrame(Form)
        self.buttonFrame.setStyleSheet("background-color: rgb(54, 69, 79); color: white")
        self.buttonFrame.setGeometry(QtCore.QRect(15, 250, 220, 535))
        self.buttonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonFrame.setObjectName("buttonFrame")

        self.siradaBekleyen = QtWidgets.QLabel(self.buttonFrame)
        self.siradaBekleyen.setGeometry(QtCore.QRect(15, 100, 175, 16))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        self.siradaBekleyen.setFont(font)
        self.siradaBekleyen.setObjectName("siradaBekleyen")

        self.oncelikliBekleyen = QtWidgets.QLabel(self.buttonFrame)
        self.oncelikliBekleyen.setGeometry(QtCore.QRect(15, 150, 175, 16))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        self.oncelikliBekleyen.setFont(font)
        self.oncelikliBekleyen.setObjectName("oncelikliBekleyen")

        self.siradakiSayi = QtWidgets.QLabel(self.buttonFrame)
        self.siradakiSayi.setGeometry(QtCore.QRect(150, 100, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setBold(True)
        font.setWeight(75)
        self.siradakiSayi.setFont(font)
        self.siradakiSayi.setObjectName("siradakiSayi")

        self.oncelikliSayi = QtWidgets.QLabel(self.buttonFrame)
        self.oncelikliSayi.setGeometry(QtCore.QRect(200, 150, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setBold(True)
        font.setWeight(75)
        self.oncelikliSayi.setFont(font)
        self.oncelikliSayi.setObjectName("oncelikliSayi")

        self.addCustomer = QtWidgets.QPushButton(self.buttonFrame)
        self.addCustomer.setStyleSheet("background-color: rgb(32,32,32)")
        self.addCustomer.clicked.connect(self.addCustomerClicked)
        self.addCustomer.setGeometry(QtCore.QRect(50, 250, 120, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addCustomer.setFont(font)
        self.addCustomer.setObjectName("addCustomer")

        self.nextStep = QtWidgets.QPushButton(self.buttonFrame)
        self.nextStep.setStyleSheet("background-color: rgb(32,32,32)")
        self.nextStep.clicked.connect(self.start_threads)
        self.nextStep.setGeometry(QtCore.QRect(50, 330, 120, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nextStep.setFont(font)
        self.nextStep.setObjectName("nextStep")

        self.end = QtWidgets.QPushButton(self.buttonFrame)
        self.end.setStyleSheet("background-color: rgb(32,32,32)")
        self.end.clicked.connect(self.stop_threads)
        self.end.setGeometry(QtCore.QRect(50, 410, 120, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.end.setFont(font)
        self.end.setObjectName("end")

        self.masalar = {
            1: self.masa1,
            2: self.masa2,
            3: self.masa3,
            4: self.masa4,
            5: self.masa5,
            6: self.masa6
        }

        self.garsonlar = {
            1: self.garson1,
            2: self.garson2,
            3: self.garson3
        }

        self.ascilar = {
            1: self.asci1,
            2: self.asci2
        }

        
        self.garsonThreads = []
        self.asciThreads = []
        self.kasiyerThread = None

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def musteriF(self, musteriThreads):
        global girisYapanMusteri
        with open(txtDosya, 'a') as txt:
            txt.write(f"{musteriThreads} siraya girdi\n")
        oncelikDegeri = random.randint(0, 1)
        musteriOncelik.put((oncelikDegeri, musteriThreads))
        oncelikliSira.append(oncelikDegeri)
        girisYapanMusteri += 1
        if girisYapanMusteri == 10:
            for _ in range(6):
                masaMultiplex.signal()

        masaMultiplex.wait()

        kullanıcı = musteriOncelik.get()
        for i, mutex in enumerate(masaMutexList, start=1):
            if mutex.signal_count == 1:
                self.masa(i, kullanıcı[1])
                break

        self.siradakiSayi.setText(str(musteriOncelik.qsize()))

        oncelikliSayi = sum(1 for oncelik, _ in list(musteriOncelik.queue) if oncelik == 0)
        self.oncelikliSayi.setText(str(oncelikliSayi))

    def masa(self, masaNo, musteriName):
        masaMutexList[masaNo - 1].wait()
        masaNumber = self.masalar[masaNo]

        if masaMutexList[masaNo - 1].signal_count == 0 and oncelikliSira[masaNo - 1] == 0:
            masaNumber.setText(f"{musteriName}\nÖncelikli")
            masaNumber.setStyleSheet("background-color: red")
        elif masaMutexList[masaNo - 1].signal_count == 0 and oncelikliSira[masaNo - 1] == 1:
            masaNumber.setText(f"{musteriName}\nNormal")
            masaNumber.setStyleSheet("background-color: red")
        else:
            masaNumber.setText(f"Masa {masaNo}")
            masaNumber.setStyleSheet("background-color: green")
        with open(txtDosya, 'a') as txt:
            txt.write(f"{musteriName} masa{masaNo} e oturdu\n")
        garsonSiparisSira.put(masaNo)
        garsonSira.append(masaNo)
        garsonMutex.signal()

    def garson(self, garsonName):
        global garsonSay, kasiyerCikisBayragi
        while not kasiyerCikisBayragi:
            garsonMutex.wait()
            garsonSay += 1
            masaNo = garsonSiparisSira.get()
            garsonNo = int(garsonName[6])
            garsonNumber = self.garsonlar[garsonNo]

            if 1 <= masaNo <= 6 and masaSiparisDurumList[masaNo - 1].signal_count == 1:
                masaSiparisDurumList[masaNo - 1].wait()
                asciYemekHazirlama.put(masaNo)
                asciSira.append(masaNo)
                with open(txtDosya, 'a') as txt:
                    txt.write(f"{garsonName} masa{masaNo} siparisini aliyor" + '\n')
                time.sleep(2)
                if garsonSiparisDurumuMutex.signal_count == 0:
                    garsonNumber.setStyleSheet("background-color: green")
                else:
                    garsonNumber.setStyleSheet("background-color: blue")
                time.sleep(2)
                asciMutex.signal()
                garsonNumber.setStyleSheet("background-color: green")
            else:
                with open(txtDosya, 'a') as txt:
                    txt.write("Siparis alinmayan masa kalmadi" + '\n')
                garsonSay -= 1
                garsonMutex.signal()

    def asci(self, asciName):
        global asciYemekSay, garsonSay, girisYapanMusteri
        asciMutex.wait()
        with open(txtDosya, 'a') as txt:
            txt.write(f"{asciName} yemekleri hazirlamaya basliyor" + '\n')
        asciNo = int(asciName[4])

        while garsonSay > 0 or girisYapanMusteri < 10:
            if garsonSay > 0:
                asciYemekSay -= 1
                masaNumarasi = asciYemekHazirlama.get()
                asciNumber = self.ascilar[asciNo] #asci threadleri 1 kez çalışıyor bunu düzelt
                kasiyerOdemeAlma.put(masaNumarasi)
                with open(txtDosya, 'a') as txt:
                    txt.write(f"{asciName} masa{masaNumarasi} in yemegini hazirliyor" + '\n')
                if asciYemekSay == 1:
                    asciNumber.setStyleSheet("background-color: yellow; color: black")
                elif asciYemekSay == 0:
                    asciNumber.setStyleSheet("background-color: red")
                else:
                    asciNumber.setStyleSheet("background-color: green")
                time.sleep(3)
                asciNumber.setStyleSheet("background-color: green")
                with open(txtDosya, 'a') as txt:
                    txt.write(f"masa{masaNumarasi} in yemegi hazir" + '\n')
                garsonSay -= 1
                asciYemekSay = 2
                garsonMutex.signal()
                time.sleep(3)
                with open(txtDosya, 'a') as txt:
                    txt.write(f"masa{masaNumarasi} deki musteri yemegini yedi" + '\n')
                kasiyerMutex.signal()
            else:
                with open(txtDosya, 'a') as txt:
                    txt.write("Tum garsonlar dolu" + '\n')
        
        asciMutex.signal()

    def kasiyer(self):
        global kasiyerCikisBayragi
        kasiyerMutex.wait()
        while not kasiyerCikisBayragi:
            try:
                odemeAlindi = kasiyerOdemeAlma.get()
                masaNumber = self.masalar[odemeAlindi]
                masaNumber.setStyleSheet("background-color: green")
                masaNumber.setText(f"Masa {odemeAlindi}")
                time.sleep(1)
                self.kasiyerCikti.append(f"Masa {odemeAlindi} ödeme alındı")
                with open(txtDosya, 'a') as txt:
                    txt.write(f"Odeme alindi, masa{odemeAlindi} hesabi kapatildi" + '\n')
                masaSiparisDurum = masaSiparisDurumList[odemeAlindi - 1]
                masaMutex = masaMutexList[odemeAlindi - 1]
                masaSiparisDurum.signal()
                masaMutex.signal()
                masaMultiplex.signal()
            except queue.Empty:
                kasiyerCikisBayragi = True  

    def addCustomerClicked(self):
        musteri = []
        rand = random.randint(1,11)
        for _ in range(rand):
            musteriIsim = f"musteri{_+10}"
            musteri.append(musteriIsim)

        for _ in range(rand):
            musteri[_] = threading.Thread(target=self.musteriF, daemon=True, args=(musteri[_],))

        for _ in range(rand):
            musteri[_].start()

    def start_threads(self):
        for i in range(10):
            musteriIsim = f"musteri{i}"
            musteriThreads.append(musteriIsim)

        for i in range(1, 4):
            garsonIsim = f"garson{i}"
            self.garsonThreads.append(garsonIsim)

        for i in range(1, 3):
            asciIsim = f"asci{i}"
            self.asciThreads.append(asciIsim)

        for i in range(10):
            musteriThreads[i] = threading.Thread(target=self.musteriF, args=(musteriThreads[i],))

        for i in range(3):
            self.garsonThreads[i] = threading.Thread(target=self.garson, args=(self.garsonThreads[i],))

        for i in range(2):
            self.asciThreads[i] = threading.Thread(target=self.asci, args=(self.asciThreads[i],))

        self.kasiyerThread = threading.Thread(target=self.kasiyer, daemon=True)

        for i in range(10):
            musteriThreads[i].start()

        for i in range(3):
            self.garsonThreads[i].start()

        for i in range(2):
            self.asciThreads[i].start()

        self.kasiyerThread.start()

    def stop_threads(self, Form):

        self.musteriFrame.close()
        self.garsonFrame.close()
        self.asciFrame.close()
        self.kasiyerFrame.close()
        self.buttonFrame.close()
        Form.setVisible(False)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "1. Mod"))
        self.masa1.setText(_translate("Form", "Masa 1"))
        self.masa2.setText(_translate("Form", "Masa 2"))
        self.masa3.setText(_translate("Form", "Masa 3"))
        self.masa4.setText(_translate("Form", "Masa 4"))
        self.masa5.setText(_translate("Form", "Masa 5"))
        self.masa6.setText(_translate("Form", "Masa 6"))
        self.garson1.setText(_translate("Form", "Garson 1"))
        self.garson2.setText(_translate("Form", "Garson 2"))
        self.garson3.setText(_translate("Form", "Garson 3"))
        self.asci1.setText(_translate("Form", "Aşçı 1"))
        self.asci2.setText(_translate("Form", "Aşçı 2"))
        self.kasiyerText.setText(_translate("Form", "Kasiyer"))
        self.siradaBekleyen.setText(_translate("Form", "Sıradaki Müşteriler :"))
        self.oncelikliBekleyen.setText(_translate("Form", "Bekleyen Öncelikli Müşteriler :"))
        self.siradakiSayi.setText(_translate("Form", "0"))
        self.oncelikliSayi.setText(_translate("Form", "0"))
        self.addCustomer.setText(_translate("Form", "Müşteri Gönder"))
        self.nextStep.setText(_translate("Form", "Sonraki Adım"))
        self.end.setText(_translate("Form", "Sonlandır"))
