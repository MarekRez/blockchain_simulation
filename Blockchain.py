import hashlib
import time
import random

# Definujeme roly používateľov
ROLE_MANAGER = "manažér"
ROLE_DRIVER = "vodič"
ROLE_CUSTOMS = "colný úradník"

class Pouzivatel:
    def __init__(self, meno, rola):
        self.meno = meno
        self.rola = rola

class Blok:
    def __init__(self, index, predchadzajuci_hash, zasielka_id, stav, majitel, miesto, casova_peciatka, schvalene, akcia):
        self.index = index
        self.predchadzajuci_hash = predchadzajuci_hash
        self.zasielka_id = zasielka_id
        self.stav = stav
        self.majitel = majitel
        self.miesto = miesto
        self.casova_peciatka = casova_peciatka
        self.schvalene = schvalene
        self.akcia = akcia
        self.nonce = 0
        self.hash = self.vytaz_hash()

    def vypocitaj_hash(self):
        sha = hashlib.sha256()
        sha.update(f"{self.index}{self.predchadzajuci_hash}{self.zasielka_id}{self.stav}{self.majitel}{self.miesto}{self.casova_peciatka}{self.schvalene}{self.akcia}{self.nonce}".encode('utf-8'))
        return sha.hexdigest()

    def vytaz_hash(self):
        hash = self.vypocitaj_hash()
        while not hash.startswith('00000'):  # Zvýšenie náročnosti na 5 nul
            self.nonce += 1
            hash = self.vypocitaj_hash()
        return hash

class InteligentnaZmluva:
    def __init__(self, minimalna_uroven_schvalenia=2):
        self.minimalna_uroven_schvalenia = minimalna_uroven_schvalenia

    def schval_akciu(self, uroven_schvalenia):
        return uroven_schvalenia >= self.minimalna_uroven_schvalenia

class Uzol:
    def __init__(self, meno):
        self.meno = meno

    def hlasuj(self, blok):
        # Náhodne simulujeme, či uzol hlasuje za alebo proti (pre zjednodušenie)
        return random.choice([True])

class Blockchain:
    def __init__(self):
        self.retazec = [self.vytvor_genesis_blok()]
        self.pristupove_pravidla = {
            "pridaj_zasielku": [ROLE_MANAGER],
            "aktualizuj_miesto": [ROLE_DRIVER],
            "prenesenie_majetku": [ROLE_MANAGER],
            "nahlad_na_udaje": [ROLE_MANAGER, ROLE_DRIVER, ROLE_CUSTOMS]
        }
        self.uzly = [Uzol(f"Uzol_{i}") for i in range(5)]  # Vytvárame 5 uzlov
        self.zmluva = InteligentnaZmluva(minimalna_uroven_schvalenia=2)

    def vytvor_genesis_blok(self):
        return Blok(0, "0", "Genesis Zásielka", "Pripravená", "Genesis Majiteľ", "Genesis Miesto", time.time(), True, "Genesis Akcia")

    def over_opravnenie(self, pouzivatel, akcia):
        povolene_roly = self.pristupove_pravidla.get(akcia, [])
        if pouzivatel.rola in povolene_roly:
            return True
        print(f"Prístup zamietnutý pre používateľa {pouzivatel.meno} s rolou {pouzivatel.rola} pre akciu '{akcia}'")
        return False

    def ziskaj_konsenzus(self, blok):
        hlasy = [uzol.hlasuj(blok) for uzol in self.uzly]
        pocet_za = hlasy.count(True)
        pocet_proti = hlasy.count(False)
        print(f"Konsenzus - Počet hlasov ZA: {pocet_za}, PROTI: {pocet_proti}")
        return pocet_za > pocet_proti

    def pridaj_zasielku(self, pouzivatel, zasielka_id, stav, majitel, miesto):
        if not self.over_opravnenie(pouzivatel, "pridaj_zasielku"):
            return
        novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, stav, majitel, miesto, time.time(), True, "Pridanie Zásielky")

        # Získať konsenzus od uzlov
        if self.ziskaj_konsenzus(novy_blok):
            self.retazec.append(novy_blok)
            print(f"Blok pridaný používateľom {pouzivatel.meno}: ID zásielky {zasielka_id} - Akcia: Pridanie Zásielky")
        else:
            print(f"Konsenzus nebol dosiahnutý. Blok s ID zásielky {zasielka_id} nebol pridaný.")

    def aktualizuj_miesto(self, pouzivatel, zasielka_id, nove_miesto):
        if not self.over_opravnenie(pouzivatel, "aktualizuj_miesto"):
            return
        for blok in reversed(self.retazec):
            if blok.zasielka_id == zasielka_id:
                novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, blok.stav, blok.majitel, nove_miesto, time.time(), True, "Aktualizácia Miesta")

                # Získať konsenzus od uzlov
                if self.ziskaj_konsenzus(novy_blok):
                    self.retazec.append(novy_blok)
                    print(f"Miesto zásielky {zasielka_id} bolo aktualizované na {nove_miesto} používateľom {pouzivatel.meno}.")
                else:
                    print(f"Konsenzus nebol dosiahnutý. Aktualizácia miesta zásielky {zasielka_id} nebola vykonaná.")
                return
        print(f"Zásielka s ID {zasielka_id} nebola nájdená v blockchainu.")

    def prenos_majetku(self, pouzivatel, zasielka_id, novy_majitel):
        if not self.over_opravnenie(pouzivatel, "prenesenie_majetku"):
            return
        for blok in reversed(self.retazec):
            if blok.zasielka_id == zasielka_id:
                novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, blok.stav, novy_majitel, blok.miesto, time.time(), True, "Prenos Majetku")

                # Získať konsenzus od uzlov
                if self.ziskaj_konsenzus(novy_blok):
                    self.retazec.append(novy_blok)
                    print(f"Majiteľ zásielky {zasielka_id} bol zmenený na {novy_majitel} používateľom {pouzivatel.meno}.")
                else:
                    print(f"Konsenzus nebol dosiahnutý. Prenos majiteľa zásielky {zasielka_id} nebol vykonaný.")
                return
        print(f"Zásielka s ID {zasielka_id} nebola nájdená v blockchainu.")

    def ziskaj_historiu_zasielky(self, zasielka_id):
        historia = [blok for blok in self.retazec if blok.zasielka_id == zasielka_id]
        if historia:
            print(f"História transakcií pre zásielku {zasielka_id}:")
            for blok in historia:
                print(f"Index: {blok.index}, Akcia: {blok.akcia}, Majiteľ: {blok.majitel}, Miesto: {blok.miesto}, Časová Pečiatka: {blok.casova_peciatka}, Schválené: {blok.schvalene}")
        else:
            print(f"História pre zásielku s ID {zasielka_id} nebola nájdená.")

    def je_retazec_platny(self):
        for i in range(1, len(self.retazec)):
            aktualny_blok = self.retazec[i]
            predchadzajuci_blok = self.retazec[i - 1]

            if aktualny_blok.hash != aktualny_blok.vypocitaj_hash():
                return False

            if aktualny_blok.predchadzajuci_hash != predchadzajuci_blok.hash:
                return False
        return True

# Vytvorenie používateľov
manazer = Pouzivatel("Ján Manažér", ROLE_MANAGER)
vodic = Pouzivatel("Peter Vodič", ROLE_DRIVER)

# Vytvorenie blockchainu
prepravny_blockchain = Blockchain()

# Pridanie aspoň 10 blokov
for i in range(10):
    prepravny_blockchain.pridaj_zasielku(manazer, f"Z{i+1:04}", "Na ceste", f"Dopravná Spoločnosť {chr(65 + i % 3)}", f"Prístav {chr(65 + i % 3)}")

# Získanie histórie zásielky
prepravny_blockchain.ziskaj_historiu_zasielky("Z0001")

# Kontrola, či je blockchain platný
print("Je blockchain platný?", prepravny_blockchain.je_retazec_platny())

# Zobrazenie blockchainu
for blok in prepravny_blockchain.retazec:
    print(f"Index: {blok.index}")
    print(f"Predchádzajúci Hash: {blok.predchadzajuci_hash}")
    print(f"ID Zásielky: {blok.zasielka_id}")
    print(f"Stav: {blok.stav}")
    print(f"Majiteľ: {blok.majitel}")
    print(f"Miesto: {blok.miesto}")
    print(f"Časová Pečiatka: {blok.casova_peciatka}")
    print(f"Schválené: {blok.schvalene}")
    print(f"Akcia: {blok.akcia}")
    print(f"Hash: {blok.hash}")
    print("-------------")
    print("-------------")

