from PyQt5 import uic
import os

# UI dosyalarının bulunduğu klasör yolu
ui_klasoru = "path .py files"

# UI dosyalarının listesini al
ui_dosyalari = [dosya for dosya in os.listdir(ui_klasoru) if dosya.endswith(".ui")]

# Her bir UI dosyasını Python koduna çevir ve aynı klasöre kaydet
for ui_dosyasi in ui_dosyalari:
    ui_dosya_yolu = os.path.join(ui_klasoru, ui_dosyasi)
    python_dosya_adi = os.path.splitext(ui_dosyasi)[0] + ".py"
    python_dosya_yolu = os.path.join(ui_klasoru, python_dosya_adi)

    with open(python_dosya_yolu, "w", encoding="utf-8") as fout:
        uic.compileUi(ui_dosya_yolu, fout)
