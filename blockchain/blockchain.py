import time
import pandas as pd
from .block import Blok
from .encryption import EncryptionManager
from .permissions import ROLE_MANAGER, ROLE_DRIVER, ROLE_CUSTOMS
from .smart_contract import InteligentnaZmluva
from .consensus import Uzol

class Blockchain:
    _instance = None  # Premenná na uloženie jedinej inštancie

    def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(Blockchain, cls).__new__(cls)
                cls._instance._initialized = False  # Kontrola, či už bol inicializovaný
            return cls._instance

    def __init__(self):
        if not self._initialized:  # Inicializujeme len raz
            self.obtiaznost = 3  # Počiatočná obtiažnosť (počet núl)
            self.encryption_manager = EncryptionManager()  # Inicializujeme správcu šifrovania
            self.retazec = [self.vytvor_genesis_blok()]
            self.pristupove_pravidla = {
                "pridaj_zasielku": [ROLE_MANAGER],
                "aktualizuj_miesto": [ROLE_DRIVER],
                "prenesenie_majetku": [ROLE_MANAGER],
                "nahlad_na_udaje": [ROLE_MANAGER, ROLE_DRIVER, ROLE_CUSTOMS]
            }
            self.uzly = [Uzol(f"Uzol_{i}") for i in range(5)]  # Simulujeme 5 uzlov
            self.zmluva = InteligentnaZmluva(minimalna_uroven_schvalenia=2)

    def vytvor_genesis_blok(self):
        return Blok(0, "0", "Genesis Zásielka", "Pripravená", "Genesis Majiteľ", "Genesis Miesto", time.time(), True, "Genesis Akcia", self.obtiaznost, self.encryption_manager)

    def aktualizuj_obtiaznost(self, novy_blok):
        target = 5.0  # Cieľový čas ťažby v sekundách
        if len(self.retazec) < 2:
            return
        predchadzajuci_blok = self.retazec[-2]
        time_taken = novy_blok.casova_peciatka - predchadzajuci_blok.casova_peciatka
        if time_taken < target and self.obtiaznost < 5:
            self.obtiaznost += 1
        elif time_taken > target and self.obtiaznost > 1:
            self.obtiaznost -= 1
        print(f"Aktualizovaná obtiažnosť: {self.obtiaznost}")

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
        novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, stav, majitel, miesto, time.time(), True, "Pridanie Zásielky", self.obtiaznost, self.encryption_manager)
        if self.ziskaj_konsenzus(novy_blok):
            self.retazec.append(novy_blok)
            print(f"Blok pridaný používateľom {pouzivatel.meno}: ID zásielky {zasielka_id} - Akcia: Pridanie Zásielky")
            self.aktualizuj_obtiaznost(novy_blok)
        else:
            print(f"Konsenzus nebol dosiahnutý. Blok s ID zásielky {zasielka_id} nebol pridaný.")

    def aktualizuj_miesto(self, pouzivatel, zasielka_id, nove_miesto):
        if not self.over_opravnenie(pouzivatel, "aktualizuj_miesto"):
            return
        for blok in reversed(self.retazec):
            if self.encryption_manager.decrypt_data(blok.zasielka_id) == zasielka_id:
                novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, self.encryption_manager.decrypt_data(blok.stav), self.encryption_manager.decrypt_data(blok.majitel), nove_miesto, time.time(), True, "Aktualizácia Miesta", self.obtiaznost, self.encryption_manager)
                if self.ziskaj_konsenzus(novy_blok):
                    self.retazec.append(novy_blok)
                    print(f"Miesto zásielky {zasielka_id} bolo aktualizované na {nove_miesto} používateľom {pouzivatel.meno}.")
                    self.aktualizuj_obtiaznost(novy_blok)
                else:
                    print(f"Konsenzus nebol dosiahnutý. Aktualizácia miesta zásielky {zasielka_id} nebola vykonaná.")
                return
        print(f"Zásielka s ID {zasielka_id} nebola nájdená v blockchainu.")

    def prenos_majetku(self, pouzivatel, zasielka_id, novy_majitel):
        if not self.over_opravnenie(pouzivatel, "prenesenie_majetku"):
            return
        for blok in reversed(self.retazec):
            if self.encryption_manager.decrypt_data(blok.zasielka_id) == zasielka_id:
                novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, self.encryption_manager.decrypt_data(blok.stav), novy_majitel, self.encryption_manager.decrypt_data(blok.miesto), time.time(), True, "Prenos Majetku", self.obtiaznost, self.encryption_manager)
                if self.ziskaj_konsenzus(novy_blok):
                    self.retazec.append(novy_blok)
                    print(f"Majiteľ zásielky {zasielka_id} bol zmenený na {novy_majitel} používateľom {pouzivatel.meno}.")
                    self.aktualizuj_obtiaznost(novy_blok)
                else:
                    print(f"Konsenzus nebol dosiahnutý. Prenos majiteľa zásielky {zasielka_id} nebol vykonaný.")
                return
        print(f"Zásielka s ID {zasielka_id} nebola nájdená v blockchainu.")

    def pridaj_kontrolu_kvality(self, pouzivatel, zasielka_id, teplota, vlhkost, poznamka):
        quality_info = f"Kontrola Kvality: teplota={teplota}, vlhkosť={vlhkost}, poznámka={poznamka}"
        if not self.over_opravnenie(pouzivatel, "nahlad_na_udaje"):
            return
        novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, "Kontrola Kvality", "-", "-", time.time(), True, quality_info, self.obtiaznost, self.encryption_manager)
        if self.ziskaj_konsenzus(novy_blok):
            self.retazec.append(novy_blok)
            print(f"Kontrola kvality pridaná pre zásielku {zasielka_id} používateľom {pouzivatel.meno}.")
            self.aktualizuj_obtiaznost(novy_blok)
        else:
            print(f"Konsenzus nebol dosiahnutý. Kontrola kvality pre zásielku {zasielka_id} nebola pridaná.")

    def predikuj_eta(self, vzdialenost_km, rychlost_kmh):
        eta_hodiny = vzdialenost_km / rychlost_kmh
        eta_sec = eta_hodiny * 3600
        print(f"Odhadovaný čas doručenia: {eta_sec} sekúnd")
        return eta_sec

    def ziskaj_historiu_zasielky(self, zasielka_id):
        # Porovnávame dešifrovanú hodnotu zásielka_id
        historia = [blok for blok in self.retazec if self.encryption_manager.decrypt_data(blok.zasielka_id) == zasielka_id]
        if historia:
            print(f"História transakcií pre zásielku {zasielka_id}:")
            for blok in historia:
                payload = blok.decrypt_payload(self.encryption_manager)
                print(f"Index: {blok.index}, Akcia: {payload['akcia']}, Majiteľ: {payload['majitel']}, Miesto: {payload['miesto']}, Časová Pečiatka: {blok.casova_peciatka}, Schválené: {blok.schvalene}")
        else:
            print(f"História pre zásielku s ID {zasielka_id} nebola nájdená.")

    def ziskaj_historiu_majitelov_a_miest(self, zasielka_id):
        historia = [blok for blok in self.retazec if self.encryption_manager.decrypt_data(blok.zasielka_id) == zasielka_id]
        if historia:
            print(f"História majiteľov a miest pre zásielku {zasielka_id}:")
            for blok in historia:
                payload = blok.decrypt_payload(self.encryption_manager)
                print(f"Index: {blok.index} - Majiteľ: {payload['majitel']}, Miesto: {payload['miesto']}")
        else:
            print(f"Pre zásielku s ID {zasielka_id} neboli nájdené žiadne záznamy.")

    def je_retazec_platny(self):
        for i in range(1, len(self.retazec)):
            aktualny_blok = self.retazec[i]
            predchadzajuci_blok = self.retazec[i - 1]
            if aktualny_blok.hash != aktualny_blok.vypocitaj_hash():
                return False
            if aktualny_blok.predchadzajuci_hash != predchadzajuci_blok.hash:
                return False
        return True

    def zobraz_sifrovane_udaje(self):
        print("\n--- Šifrované údaje v blockchainu ---")
        for blok in self.retazec:
            print(f"Index: {blok.index}")
            print(f"Predchádzajúci Hash: {blok.predchadzajuci_hash}")
            print(f"ID Zásielky (šifrované): {blok.zasielka_id}")
            print(f"Stav (šifrované): {blok.stav}")
            print(f"Majiteľ (šifrované): {blok.majitel}")
            print(f"Miesto (šifrované): {blok.miesto}")
            print(f"Časová Pečiatka: {blok.casova_peciatka}")
            print(f"Schválené: {blok.schvalene}")
            print(f"Akcia (šifrované): {blok.akcia}")
            print(f"Hash: {blok.hash}")
            print("-------------")

    def ziskaj_data(self):
        data = []
        for blok in self.retazec:
            payload = blok.decrypt_payload(self.encryption_manager)
            data.append([blok.index, payload['zasielka_id'], payload['stav'], payload['majitel'], payload['miesto'], payload['akcia'], blok.casova_peciatka])
        return pd.DataFrame(data, columns=["Index", "ID Zásielky", "Stav", "Majiteľ", "Miesto", "Akcia", "Časová Pečiatka"])