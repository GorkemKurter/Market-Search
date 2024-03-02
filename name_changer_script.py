import os


klasor_yolu = r'C:\Users\gorkemk\PycharmProjects\Market-Search\marketscrapping\HTML Files\wdmediamarktDE'

for dosya_adi in os.listdir(klasor_yolu):
    if dosya_adi.endswith('.txt'):
        dosya_temeli, dosya_uzantisi = os.path.splitext(dosya_adi)
        yeni_dosya_adi = dosya_temeli + '.html'
        os.rename(os.path.join(klasor_yolu, dosya_adi), os.path.join(klasor_yolu, yeni_dosya_adi))

