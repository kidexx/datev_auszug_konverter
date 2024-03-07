# Importieren der benötigten Module
import csv
import re
import datetime
import _strptime
from datetime import date
from itertools import islice
#from tkinter import filedialog
#from tkinter import *
#import tkinter as tk
from pathlib import Path
import configparser



def n26(file_in, file_out, bic, iban):
        #N26
        
        # Öffnen der Eingabedatei im Lese-Modus
        with open(file_in, "r") as eingabe:
            # Erstellen eines CSV-Lesers mit dem Semikolon als Trennzeichen
            reader = csv.reader(eingabe, delimiter=",", quotechar='"')
            # Öffnen der Ausgabedatei im Schreib-Modus
            with open(file_out, "w", newline='') as ausgabe:
                # Erstellen eines CSV-Schreibers mit dem Komma als Trennzeichen
                writer = csv.writer(ausgabe, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                # Schreiben der Kopfzeile in die Ausgabedatei
                # Die Kopfzeile besteht aus den Spaltennamen, die in der Seite beschrieben sind
                # 
                # Iterieren über jede Zeile in der Eingabedatei
                for zeile in islice(reader, 1, None):
                    #print(zeile)
                    # Erstellen einer leeren Liste für die neue Zeile
                    neue_zeile = []
                    date_str = zeile[0]
                    date_format = '%Y-%m-%d'
                    date_obj = datetime.datetime.strptime(date_str, date_format)
                    date_str_buchung = date_obj.strftime('%d.%m.%Y')
                    date_obj = date.today()
                    date_str_heute = date_obj.strftime('%d.%m.%Y')
                    neue_zeile.append(bic) # N26, muss
                    neue_zeile.append(iban) # N26, muss
                    neue_zeile.append('') # Auszugsnummer, kann
                    neue_zeile.append('')  # Auszugsdatum, kann
                    neue_zeile.append('')  # Valuta, kann
                    neue_zeile.append(date_str_buchung) # Buchungsdatum, muss
                    # Umsatz, muss
                    #print(zeile[0]+' ~ '+zeile[1]+' ~ '+zeile[2]+' ~ '+zeile[3]+' ~ '+zeile[4]+' ~ '+zeile[5]+' ~ '+zeile[6])
                    if zeile[5] == '':
                        umsatz = 0
                    else:
                        umsatz = float(zeile[5])
                    #print(zeile[5])
                    #print(umsatz)
                    neue_zeile.append(umsatz) # Umsatz
                    neue_zeile.append(zeile[1][0:27]) # Zahlungspartners  max 27 zeichen, 1. Teil, kann
                    neue_zeile.append(zeile[1][27:54]) # Zahlungspartners  max 27 zeichen, 2. Teil, kann
                    neue_zeile.append('') # Bankleitzahl oder BIC des Auftraggebers , kann
                    neue_zeile.append(zeile[2]) # Kontonummer oder IBAN des Auftraggebers , kann
                    neue_zeile.append(zeile[4][0:27]) # Verwendungszweck 1  max 27 zeichen, kann
                    neue_zeile.append(zeile[4][27:54]) # Verwendungszweck 2  max 27 zeichen, kann
                    neue_zeile.append(zeile[4][54:81]) # Verwendungszweck 3  max 27 zeichen, kann
                    neue_zeile.append(zeile[4][81:108]) # Verwendungszweck 4  max 27 zeichen, kann
                    neue_zeile.append('') # Geschäftsvorgangscode, 3-stelliger Code, der Hinweise auf die Zahlungsart gibt. (Z. B. "077" für eine Btx-Überweisung) , kann
                    neue_zeile.append('EUR') # Währung, kann
                    neue_zeile.append('') # Buchungstext, kann
                    neue_zeile.append(zeile[4][108:135]) # Verwendungszweck 5, kann
                    neue_zeile.append(zeile[4][135:162]) # Verwendungszweck 6, kann
                    neue_zeile.append(zeile[4][162:189]) # Verwendungszweck 7, kann
                    neue_zeile.append(zeile[4][189:216]) # Verwendungszweck 8, kann
                    neue_zeile.append(zeile[4][216:243]) # Verwendungszweck 9, kann
                    neue_zeile.append(zeile[4][243:270]) # Verwendungszweck 10, kann
                    neue_zeile.append('') # Ursprungsbetrag, kann
                    neue_zeile.append('') # Währung Ursprungsbetrag, kann
                    neue_zeile.append('') # Äquivalenzbetrag, kann
                    neue_zeile.append('') # Währung Äquivalenzbetrag, kann
                    neue_zeile.append('') # Gebühr, kann
                    neue_zeile.append('') # Währung Gebühr, kann
                    neue_zeile.append(zeile[4][270:297]) # Verwendungszweck 11, kann
                    neue_zeile.append(zeile[4][297:324]) # Verwendungszweck 12, kann
                    neue_zeile.append(zeile[4][324:351]) # Verwendungszweck 13, kann
                    neue_zeile.append(zeile[4][351:378]) # Verwendungszweck 14, kann


                    writer.writerow(neue_zeile)
        print('fertig')

        
def migros(file_in, file_out, bic, iban):
        # Das Buchungsdatum der Bankkontoumsätze muss innerhalb der Datei aufsteigend sortiert sein
        # (d. h. der älteste Kontoumsatz steht am Anfang, der aktuellste Umsatz am Ende der Datei).

        

        # Öffnen der Eingabedatei im Lese-Modus
        with open(file_in, "r") as eingabe:
            # Erstellen eines CSV-Lesers mit dem Semikolon als Trennzeichen
            reader = csv.reader(eingabe, delimiter=";", quotechar='"')
            neue_zeilen = []
            # Öffnen der Ausgabedatei im Schreib-Modus
            with open(file_out, "w", newline='') as ausgabe:
                # Erstellen eines CSV-Schreibers mit dem Komma als Trennzeichen
                writer = csv.writer(ausgabe, delimiter=";", quotechar='"', encoding='cp1250', quoting=csv.QUOTE_NONNUMERIC)
                # Schreiben der Kopfzeile in die Ausgabedatei
                # Die Kopfzeile besteht aus den Spaltennamen, die in der Seite beschrieben sind
                # 
                # Iterieren über jede Zeile in der Eingabedatei
                for zeile in islice(reader, 12, None):
                    # Erstellen einer leeren Liste für die neue Zeile
                    neue_zeile = []
                    #print(zeile[0]+' ~ '+zeile[1]+' ~ '+zeile[2]+' ~ '+zeile[3])
                    date_str = zeile[0]
                    date_format = '%d.%m.%y'
                    date_obj = datetime.datetime.strptime(date_str, date_format)
                    date_str_buchung = date_obj.strftime('%d.%m.%Y')
                    date_obj = date.today()
                    date_str_heute = date_obj.strftime('%d.%m.%Y')
                    neue_zeile.append(bic) # Migros, muss
                    neue_zeile.append(iban) # Migros, muss
                    neue_zeile.append('') # Auszugsnummer, kann
                    neue_zeile.append('')  # Auszugsdatum, kann
                    neue_zeile.append('')  # Valuta, kann
                    neue_zeile.append(date_str_buchung) # Buchungsdatum, muss
                    # Umsatz, muss
                    #print(zeile[0]+' ~ '+zeile[1]+' ~ '+zeile[2]+' ~ '+zeile[3]+' ~ '+zeile[4]+' ~ '+zeile[5]+' ~ '+zeile[6])
                    if zeile[2] == '':
                        umsatz = 0
                    else:
                        umsatz = float(zeile[2])
                    #print(zeile[5])
                    #print(umsatz)
                    neue_zeile.append(umsatz) # Umsatz
                    neue_zeile.append('') # Zahlungspartners  max 27 zeichen, 1. Teil, kann
                    neue_zeile.append('') # Zahlungspartners  max 27 zeichen, 2. Teil, kann
                    neue_zeile.append('') # Bankleitzahl oder BIC des Auftraggebers , kann
                    neue_zeile.append('') # Kontonummer oder IBAN des Auftraggebers , kann
                    neue_zeile.append(zeile[1][0:27]) # Verwendungszweck 1  max 27 zeichen, kann
                    neue_zeile.append(zeile[1][27:54]) # Verwendungszweck 2  max 27 zeichen, kann
                    neue_zeile.append(zeile[1][54:81]) # Verwendungszweck 3  max 27 zeichen, kann
                    neue_zeile.append(zeile[1][81:108]) # Verwendungszweck 4  max 27 zeichen, kann
                    neue_zeile.append('') # Geschäftsvorgangscode, 3-stelliger Code, der Hinweise auf die Zahlungsart gibt. (Z. B. "077" für eine Btx-Überweisung) , kann
                    neue_zeile.append('CHF') # Währung, kann
                    neue_zeile.append('') # Buchungstext, kann
                    neue_zeile.append(zeile[1][108:135]) # Verwendungszweck 5, kann
                    neue_zeile.append(zeile[1][135:162]) # Verwendungszweck 6, kann
                    neue_zeile.append(zeile[1][162:189]) # Verwendungszweck 7, kann
                    neue_zeile.append(zeile[1][189:216]) # Verwendungszweck 8, kann
                    neue_zeile.append(zeile[1][216:243]) # Verwendungszweck 9, kann
                    neue_zeile.append(zeile[1][243:270]) # Verwendungszweck 10, kann
                    neue_zeile.append('') # Ursprungsbetrag, kann
                    neue_zeile.append('') # Währung Ursprungsbetrag, kann
                    neue_zeile.append('') # Äquivalenzbetrag, kann
                    neue_zeile.append('') # Währung Äquivalenzbetrag, kann
                    neue_zeile.append('') # Gebühr, kann
                    neue_zeile.append('') # Währung Gebühr, kann
                    neue_zeile.append(zeile[1][270:297]) # Verwendungszweck 11, kann
                    neue_zeile.append(zeile[1][297:324]) # Verwendungszweck 12, kann
                    neue_zeile.append(zeile[1][324:351]) # Verwendungszweck 13, kann
                    neue_zeile.append(zeile[1][351:378]) # Verwendungszweck 14, kann


                    neue_zeilen.append(neue_zeile.encode('windows-1250'))

                for x in reversed(neue_zeilen):
                    writer.writerow(x)
        print('fertig, Datei '+file_out+' erstellt.')

# config lesen
# CREATE OBJECT
config_file = configparser.ConfigParser()
# READ CONFIG FILE
config_file.read("config/config.ini")


        
# Checke alle Dateien in Verzeichnis
directory = '.'
files = Path(directory).glob('*.csv')


#config_file["K01"]["iban"])
    

for file in files:
    #print(file.name)

    if str(file.name).find('_datev') == -1:
            filename = str(file.absolute()).split(".")
            filename_datev = filename[0] + '_datev.' + filename[1]
            #print(filename_datev)
            path_datev = Path(filename_datev)
            
            if path_datev.is_file():
                    print('Datev ' + path_datev.name + ' Datei schon vorhanden, mache nichts.')
            else:
                    for each_section in config_file.sections():
                        print (each_section)
                        if str(file.name).find(config_file[each_section]["dateiname_suche"]) == 0:
                             print('Datev ' + path_datev.name + ' existiert noch nicht, starte Konvertierung:')
                             if config_file[each_section]["typ"] == 'migros':
                                     migros(file, filename_datev, config_file[each_section]["bic"], config_file[each_section]["iban"]);
                             if config_file[each_section]["typ"] == 'n26':
                                     n26(file, filename_datev, config_file[each_section]["bic"], config_file[each_section]["iban"]);

