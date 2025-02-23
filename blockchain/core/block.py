import hashlib
from blockchain.cryptography.digital_signature import podpis_transakciu, over_podpis

class Blok:
    def __init__(self, index, predchadzajuci_hash, zasielka_id, stav, majitel, miesto, casova_peciatka,
                 schvalene, akcia, obtiaznost, encryption_manager):
        self.index = index
        self.predchadzajuci_hash = predchadzajuci_hash
        self.zasielka_id = encryption_manager.encrypt_data(zasielka_id)
        self.stav = encryption_manager.encrypt_data(stav)
        self.majitel = encryption_manager.encrypt_data(majitel)
        self.miesto = encryption_manager.encrypt_data(miesto)
        self.casova_peciatka = casova_peciatka
        self.schvalene = schvalene
        self.akcia = encryption_manager.encrypt_data(akcia)
        self.nonce = 0
        self.obtiaznost = obtiaznost
        self.hash = self.vytaz_hash()
        self.podpis = podpis_transakciu(self.akcia)  # Podpis akcie
        #self.akcia = "Neautorizovaná zmena"

    def over_podpis(self):
        return over_podpis(self.akcia, self.podpis)

    def vypocitaj_hash(self):
        sha = hashlib.sha256()
        sha.update(f"{self.index}{self.predchadzajuci_hash}{self.zasielka_id}{self.stav}{self.majitel}{self.miesto}"
                   f"{self.casova_peciatka}{self.schvalene}{self.akcia}{self.nonce}".encode('utf-8'))
        return sha.hexdigest()

    def vytaz_hash(self):
        hash = self.vypocitaj_hash()
        while not hash.startswith('0' * self.obtiaznost):
            self.nonce += 1
            hash = self.vypocitaj_hash()
        return hash

    def decrypt_payload(self, encryption_manager):
        return {
            "zasielka_id": encryption_manager.decrypt_data(self.zasielka_id),
            "stav": encryption_manager.decrypt_data(self.stav),
            "majitel": encryption_manager.decrypt_data(self.majitel),
            "miesto": encryption_manager.decrypt_data(self.miesto),
            "akcia": encryption_manager.decrypt_data(self.akcia)
        }
