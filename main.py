from blockchain.blockchain import Blockchain
from blockchain.permissions import Pouzivatel, ROLE_MANAGER, ROLE_DRIVER
from blockchain.ui.dashboard import zobraz_dashboard

# Vytvorenie používateľov
manazer = Pouzivatel("Ján Manažér", ROLE_MANAGER)
vodic = Pouzivatel("Peter Vodič", ROLE_DRIVER)

# Vytvorenie blockchainu
blockchain = Blockchain()

# Pridanie aspoň 10 blokov s dynamicky generovanými údajmi
for i in range(10):
    blockchain.pridaj_zasielku(
        manazer,
        f"Z{i+1:04}",
        "Na ceste",
        f"Dopravná Spoločnosť {chr(65 + i % 3)}",
        f"Prístav {chr(65 + i % 3)}"
    )

# Pridanie kontroly kvality pre zásielku Z0001
blockchain.pridaj_kontrolu_kvality(manazer, "Z0001", 5, 60, "V poriadku")

# Predikcia ETA pre trasu 500 km pri rýchlosti 50 km/h
blockchain.predikuj_eta(500, 50)

blockchain.zobraz_sifrovane_udaje()

# Získanie histórie zásielky Z0001
blockchain.ziskaj_historiu_zasielky("Z0001")

# Získanie histórie majiteľov a miest pre zásielku Z0001
blockchain.ziskaj_historiu_majitelov_a_miest("Z0001")

# Kontrola, či je blockchain platný
print("Je blockchain platný?", blockchain.je_retazec_platny())

# Zobrazenie blockchainu (dešifrované údaje)
for blok in blockchain.retazec:
    payload = blok.decrypt_payload(blockchain.encryption_manager)
    print(f"Index: {blok.index}")
    print(f"Predchádzajúci Hash: {blok.predchadzajuci_hash}")
    print(f"ID Zásielky: {payload['zasielka_id']}")
    print(f"Stav: {payload['stav']}")
    print(f"Majiteľ: {payload['majitel']}")
    print(f"Miesto: {payload['miesto']}")
    print(f"Časová Pečiatka: {blok.casova_peciatka}")
    print(f"Schválené: {blok.schvalene}")
    print(f"Akcia: {payload['akcia']}")
    print(f"Hash: {blok.hash}")
    print("-------------")

zobraz_dashboard()