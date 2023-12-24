import re 

def extract_kilograms(product):
    match = re.search(r'(\d+(\.\d+)?)\s*kg', product, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


list = ['Lave linge hublot WGG04209FR 9kg Blanc', 'Lave-linge hublot MTWE91295WFR 9kg', 'Lave-linge hublot FP0824WC0FR 8kg Autodose', 'Lave-linge hublot ALF5081-NE 5kg', 'Lave-linge hublot F94R56WHS - 9kg', 'Lave-linge hublot F51P12WH 15 kg Blanc', 'Lave- linge hublot BWE91496XWVFR - 9kg', 'Lave-linge hublot FF0814WA0FR 8kg Blanc', 'Lave-linge hublot ALF 6124 - 6kg', 'Lave linge hublot WUV8412XBWS - 8kg', 'Lave- linge hublot WW11BBAO46AW- 11kg', 'Lave-linge hublot ALF 5104 - 5kg', 'Lave-linge hublot FFBB9469CVFR 9kg Blanc', 'Lave-linge hublot W1214QA - 12kg', 'Lave linge hublot 8kg WW80T554DAE/ES3 Addwash', 'Lave-linge hublot ALF 6122 6kg Blanc', 
'Lave linge hublot EW6F5120WS - 10kg', 'Lave linge hublot CSS1411TWMBE 11kg Blanc', 'Lave-linge hublot F24V30WHS 12 kg Blanc', 'Lave linge hublot CSS1414TWMBE 14kg Blanc', 'Lave-linge hublot WAJ24018FR 8kg Blanc', 'Lave linge hublot WUE7424W0W- 7kg', 'Lave linge hublot SLF7140ATBV -7kg', 'lave linge hublot BWE91485XWFRN 9kg Blanc', 'Lave linge hublot CS1410TXMBE/1 10 kg Blanc', 'Lave-linge hublot HW08-CPW14639N - 8kg', 'Lave-linge hublot F82AV35MB - 8,5kg', 'Lave linge hublot WGG04419FR - 9kg', 'Lave- linge hublot EW2F7144AN - 8kg', 'Lave-linge Hublot 8 kg 1400 trs/mn - Cs 1482dwb4/1-47 Blanc', 'Lave-linge hublot WFQA9014EVJM- 9kg', 'Lave-linge Frontal 60 cm 13kg 1400 trs/mn Blanc - Css1413twmre-47', 'Lave-linge hublot F71P12WH 17kg Blanc', 'Lave-linge Hublot 60 cm 9kg 1400 Tours/min classe A - Ww90t554daws3', 'Lave-linge Hublot 8 kg 1200 trs/mn - F82d13whs', 'Lave linge hublot SLF7123W-NE 7kg Blanc', 'Lave-linge Frontal Compact 5 kg 1200 trs/mn Blanc Mini Drum - 51x70x49 cm - HW50-BP12307-S', 'Lave-linge Frontal 6 kg 1200 trs/mn - Wue6612w1w', 'Lave-linge Hublot 11kg 68L 1400 trs/mn, programme vapeur anti-allergie - F14R15WHS', 'Lave-linge-frontal compact 3 kg 1000 trs/mn PerfectCare - Ewc1051', 'Lave-linge Frontal 6 kg 1200 trs/mn 39L SteamCure Silver - Wue6612s1s', 'Lave-linge hublot WW80TA046TEA - 8kg Blanc', 'Lave-linge Intégrable 9kg 1600 Tours/min - Obws69twmce-47', 'Lave-linge Hublot 11kg 1400 Tours/min Blanc - Ww11bga046aeef', 'Lave-linge 7 kg 1400 trs/mn - Technologie Ecobubble™ - Technologie Addwash™ - Ww70t554dax', 'Lave-linge Hublot 11 Kg 1400 Tours/min  - Moteur Prosmart Inverter -  Llf11w2', 'Lave-linge hublot 10 kg 1400 trs/min Smart Inverter 60 cm - Noir - Css1410twmcbe-47', 'Lave-linge Hublot 10 Kg 1400 Tours/min - CS 14102DW4/1-47', 'Lave-linge Hublot 10 Kg - 60 Cm Largeur - 1200 Trs/mn - Noir - Co12103dbbe/1-47', 'Lave linge hublot HW150-BP14986E 15 kg Blanc', 'Lave-linge hublot WQA1014EVJMT 10kg Titanium', 'Lave-linge hublot F94M21WHS 9 kg Blanc', 'Lave- linge hublot FF0914SC0FR 9kg Silver']

kilograms = []

for i in range(len(list)):
    kilograms.append(extract_kilograms(list[i]))

'''print(list[48])
print(list[47])
print(list[45])
print(list[30])
print(kilograms)
print(len(kilograms))
'''



liste = [
    '\n                                            ',
    '\n                        Lave-linge séchant 8 kg / 6 kg VALBERG WD 8615 B/E W566C                    ',
    '\n                        Lave-linge séchant 10 kg / 6 kg VALBERG WD 10614 A/D W180C                    ',
    '\n                        Lave-linge séchant 8 kg/ 6 kg WHIRLPOOL EFFWDB 864349 BV FR                    ',
    '\n                        Lave-linge séchant 9 kg / 6 kg HISENSE WD914LE                    ',
    '\n  Lave-linge séchant 8 kg / 5 kg LG F854M20WR                    '
]


def get_dry_capacity(liste):
    sondaki_sayilar = []

    for item in liste:
        match = re.search(r'/ (\d+)', item)
        if match:
            sondaki_sayilar.append(match.group(1))
    return sondaki_sayilar        



def rpm_purification(input):
    pattern = r'(\d+)'
    match = re.search(pattern,input)
    if match:
        return match.group(1)


#print(extract_kilograms("Lave-linge hublot 9kg 1400 trs/mn Classe A - Ffbs9469wvfr"))

x = '11kg - 13kg'.split("-")[1].replace(" ","").replace("kg","")

print(x)

y = [6,8]

print(len(y))
temp_name = []
none_indices = [index for index, value in enumerate(temp_name) if value is None]