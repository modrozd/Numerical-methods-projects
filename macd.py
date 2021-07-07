# Projekt nr 1 z Metod Numerycznych - MACD
# Monika Drozd 175768

# Dane historyczne: Asseco Business Solutions SA (ABS)	
# Zakres danych 01.01.2017 - 24.01.2021 (1000 dni)

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Mechanizm kupna i sprzedazy akcji
budzetStart = 1000
budzet = 1000
akcje = 0

def kup(cena):
    global budzet 
    global akcje
    budzet = budzet - cena
    akcje += 1

def sprzedaj(cena):
    global budzet
    global akcje
    budzet += cena 
    akcje -= 1

# Funkcja obliczajaca SIGNAL
def mySIGNAL(wynikiMACD, nrDanych):
    return myEMA(9, wynikiMACD, nrDanych)

# Funkcja obliczajaca EMA
def myEMA(okres, otwarcie, nrDanych):
    
    alfa = 2/(okres+1)
    podstawa = 1 - alfa
    mian = 0
    licz = 0

    for i in range(0,okres,1):
        cena_otwarcia = otwarcie[i]
        if nrDanych - i >= 0:
            x = pow(podstawa, i)
            mian += 1.0*x
            x *= otwarcie[nrDanych - i]
            licz += x

    return licz / mian


# Funkcja wywolujaca obliczanie EMA dla podanych okresow
def myMACD(dane, nrDanych, lewyOkres, prawyOkres):

    emaLeft = myEMA(lewyOkres, dane, nrDanych)
    emaRight = myEMA(prawyOkres, dane, nrDanych)
    
    return emaLeft - emaRight


# Funkcja tworzaca wykres
def myPlot(trueX, falseX, y1, y2, y3): 
    
    probka = list(range(1,len(y1)+1))

    fig,ax = plt.subplots(figsize=(8,5.5), dpi=1000)
    ax.set(xlabel='Numer próbki', ylabel='Cena otwarcia', title='Wykres wskaźnika MACD oraz SIGNAL')

    #ax.plot(probka, y1, color='red', linewidth=0.8, label='Cena otwarcia')   # wykres ceny otwarcia od daty
    ax.plot(probka, y2, color='darkorange', linewidth=0.4, label='MACD')      # wykres MACD od daty
    ax.plot(probka, y3, color='blue', linewidth=0.4, label='SIGNAL')          # wykres SIGNAL od daty
    

    plt.axvline(trueX[0], color='green', linewidth=0.08, label='Kupno')
    plt.axvline(falseX[0], color='red', linewidth=0.08, label='Sprzedaż')

    for xc in trueX:
        plt.axvline(xc, color='green', linewidth=0.08)
    for xc in falseX:
        plt.axvline(xc, color='red', linewidth=0.08)

    ax.legend()

    plt.xticks(rotation = 90)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('macd.png')
    #plt.show()


#-----------------------#
# Glowna czesc programu #
#-----------------------#

# Wczytanie danych z pliku .csv do programu
dane = np.genfromtxt("abs_d.csv", delimiter=",", skip_header=1, dtype=str, encoding='utf8')
data = dane[:,0]
otwarcie = dane[:,1].astype(float)
najwyzszy = dane[:,2].astype(float)
najnizszy = dane[:,3].astype(float)
zamkniecie = dane[:,4].astype(float)
wolumen = dane[:,5].astype(float)

wynikiMACD = []
wynikiSIGNAL = []

# Policzenie MACD oraz SIGNAL dla wybranego zestawu danych 
for i in range(0,len(dane),1):
    wynikiMACD.append(myMACD(otwarcie, i, 12, 16)) # dla ema12 - ema16

for i in range(0,len(dane),1):
    wynikiSIGNAL.append(mySIGNAL(wynikiMACD, i))


 # Symulacja automatycznego kupna/sprzedazy akcji na podstawie zmian trendu
iloscDni = 14
dzienSprzedania = []
dzienKupienia = []

for dzien in range(iloscDni,len(dane)):
    iloscDniMACD = wynikiMACD[dzien - iloscDni:dzien]
    iloscDniSIGNAL = wynikiSIGNAL[dzien - iloscDni:dzien]

    sredniaMACD = np.average(iloscDniMACD)
    sredniaSIGNAL = np.average(iloscDniSIGNAL)

    if wynikiMACD[dzien] - sredniaMACD < wynikiMACD[dzien] and wynikiMACD[dzien] > wynikiSIGNAL[dzien]:
        if akcje > 2:
            sprzedaj(otwarcie[dzien])
            sprzedaj(otwarcie[dzien])
            dzienSprzedania.append(dzien)
    elif wynikiMACD[dzien] - sredniaMACD < wynikiMACD[dzien] and wynikiMACD[dzien] < wynikiSIGNAL[dzien]:
        if budzet >= otwarcie[dzien]:
            kup(otwarcie[dzien])
            dzienKupienia.append(dzien);

for ak in range(akcje):
    sprzedaj(otwarcie[len(dane)-1])

myPlot(dzienKupienia, dzienSprzedania, otwarcie, wynikiMACD, wynikiSIGNAL)

print("Poczatkowy budzet: ", budzetStart)
print("Ilosc sprzedanych akcji: ", len(dzienSprzedania))
print("Ilosc kupionych akcji: ", len(dzienKupienia))
print("Budzet koncowy: ", budzet, "     -> Zysk: ", budzet - budzetStart)
