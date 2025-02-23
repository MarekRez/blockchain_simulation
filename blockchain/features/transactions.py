import time

from blockchain.core.block import Blok

def pridaj_zasielku(self, pouzivatel, zasielka_id, stav, majitel, miesto):
    if not self.over_opravnenie(pouzivatel, "pridaj_zasielku"):
        return

    novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, stav, majitel, miesto, time.time(),
                     True, "Pridanie Zásielky", self.obtiaznost, self.encryption_manager)

    if not novy_blok.over_podpis():
        print("Blok zamietnutý! Podpis nie je platný.")
        return

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

            novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, self.encryption_manager.decrypt_data(blok.stav),
                             self.encryption_manager.decrypt_data(blok.majitel), nove_miesto, time.time(), True,
                             "Aktualizácia Miesta", self.obtiaznost, self.encryption_manager)

            if not novy_blok.over_podpis():
                print("Blok zamietnutý! Podpis nie je platný.")
                return

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

            novy_blok = Blok(len(self.retazec), self.retazec[-1].hash, zasielka_id, self.encryption_manager.decrypt_data(blok.stav),
                             novy_majitel, self.encryption_manager.decrypt_data(blok.miesto), time.time(), True,
                             "Prenos Majetku", self.obtiaznost, self.encryption_manager)

            if not novy_blok.over_podpis():
                print("Blok zamietnutý! Podpis nie je platný.")
                return

            if self.ziskaj_konsenzus(novy_blok):
                self.retazec.append(novy_blok)
                print(f"Majiteľ zásielky {zasielka_id} bol zmenený na {novy_majitel} používateľom {pouzivatel.meno}.")
                self.aktualizuj_obtiaznost(novy_blok)
            else:
                print(f"Konsenzus nebol dosiahnutý. Prenos majiteľa zásielky {zasielka_id} nebol vykonaný.")
            return
    print(f"Zásielka s ID {zasielka_id} nebola nájdená v blockchainu.")