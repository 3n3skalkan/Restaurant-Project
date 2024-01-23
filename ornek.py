import threading, random , time, queue
from threading import Semaphore

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

musteriOncelik = queue.PriorityQueue() #gelen müşterileri ilk olarak bu kuyruk içerisine atacağız ardından öncelik değerine göre sırasıyla alacağız
garsonSiparisSira = queue.Queue() #bu kuyruk garsonların sipariş alacağı masaları bir kuyruğa koyar ve buradan sırasıyla her thread bir tane işlemi yapar
asciYemekHazirlama = queue.Queue()
kasiyerOdemeAlma = queue.Queue()

lock = threading.Lock()
i = 0
girisYapanMusteri = 0
garsonSay = 0
musteriThreads = []
garsonThreads = []
asciThreads = []
kasiyerCikisBayragi = False #True olduğunda program çıkış yapar

masaMultiplex = Semaphore(0)

masaMutexList = [Semaphore(1) for _ in range(6)]
masaSiparisDurumList = [Semaphore(1) for _ in range(6)]

garsonMutex = Semaphore(0)
garsonSiparisDurumuMutex = Semaphore(1)

asciMutex = Semaphore(0)
asciYemekSay = 2

kasiyerMutex = Semaphore(0)

def musteriF(musteriThreads):
    global girisYapanMusteri
    print(f"{musteriThreads} siraya girdi")
    oncelikDegeri = random.randint(0, 1)
    print(oncelikDegeri)
    musteriOncelik.put((oncelikDegeri, musteriThreads))
    girisYapanMusteri += 1
    if girisYapanMusteri == 10:
        for _ in range(6):
            masaMultiplex.signal()

    masaMultiplex.wait()

    kullanıcı = musteriOncelik.get()
    for i, mutex in enumerate(masaMutexList, start=1):
        if mutex.signal_count == 1:
            masa(i, kullanıcı[1])
            break

def masa(masaNo, musteriName):
    masaMutexList[masaNo - 1].wait()
    print(f"{musteriName} masa{masaNo} e oturdu")
    garsonSiparisSira.put(masaNo)
    garsonMutex.signal()

def garson(garsonName):
    global garsonSay, kasiyerCikisBayragi
    while not kasiyerCikisBayragi:
        garsonMutex.wait()
        garsonSay += 1
        masaNo = garsonSiparisSira.get()

        if 1 <= masaNo <= 6 and masaSiparisDurumList[masaNo - 1].signal_count == 1:
            masaSiparisDurumList[masaNo - 1].wait()
            asciYemekHazirlama.put(masaNo)
            print(f"{garsonName} masa{masaNo} siparisini aliyor")
            time.sleep(2)
            asciMutex.signal()
        else:
            print("Siparis alinmayan masa kalmadi")
            garsonSay -= 1
            garsonMutex.signal()

def asci(asciName):
    global asciYemekSay, garsonSay, girisYapanMusteri
    yemekSayisi = 1
    asciMutex.wait()
    print(f"{asciName} yemekleri hazirlamaya basliyor")

    while garsonSay > 0 or girisYapanMusteri < 10:
        if garsonSay > 0:
            masaNumarasi = asciYemekHazirlama.get()
            kasiyerOdemeAlma.put(masaNumarasi)
            print(f"{asciName} masa{masaNumarasi} in yemegini hazirliyor")
            time.sleep(3)
            print(f"masa{masaNumarasi} in yemegi hazir")
            garsonSay -= 1
            garsonMutex.signal()
            time.sleep(3)
            print(f"masa{masaNumarasi} deki musteri yemegini yedi")
            kasiyerMutex.signal()
        else:
            print("Tum garsonlar dolu")

    print(f"{asciName} maksimum yemek sayisina ulasti, beklemede kalacak")
    asciMutex.signal()

def kasiyer():
    global kasiyerCikisBayragi
    kasiyerMutex.wait()
    while not kasiyerCikisBayragi:
        try:
            odemeAlindi = kasiyerOdemeAlma.get()
            time.sleep(1)
            print(f"Odeme alindi, masa{odemeAlindi} hesabi kapatildi")
            masaSiparisDurum = masaSiparisDurumList[odemeAlindi - 1]
            masaMutex = masaMutexList[odemeAlindi - 1]
            masaSiparisDurum.signal()
            masaMutex.signal()
            masaMultiplex.signal()
        except queue.Empty:
            kasiyerCikisBayragi = True
    print("Kasiyer exiting...")

for i in range(10):
    musteriIsim = f"musteri{i}"
    musteriThreads.append(musteriIsim)

for i in range(1, 4):
    garsonIsim = f"garson{i}"
    garsonThreads.append(garsonIsim)

for i in range(1, 3):
    asciIsim = f"asci{i}"
    asciThreads.append(asciIsim)

for i in range(10):
    musteriThreads[i] = threading.Thread(target=musteriF, args=(musteriThreads[i],))

for i in range(3):
    garsonThreads[i] = threading.Thread(target=garson, args=(garsonThreads[i],))

for i in range(2):
    asciThreads[i] = threading.Thread(target=asci, args=(asciThreads[i],))

kasiyerThread = threading.Thread(target=kasiyer)

for i in range(10):
    musteriThreads[i].start()

for i in range(3):
    garsonThreads[i].start()

for i in range(2):
    asciThreads[i].start()

kasiyerThread.start()

for i in range(3):
    garsonThreads[i].join()

for i in range(2):
    asciThreads[i].join()

for i in range(10):
    musteriThreads[i].join()

kasiyerThread.join()