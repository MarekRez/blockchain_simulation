import os

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

KEYS_DIR = os.path.join(os.path.dirname(__file__), "private_key.pem")
KEYS_DIR2 = os.path.join(os.path.dirname(__file__), "public_key.pem")

# Načítanie súkromného kľúča
def nacitaj_sukromny_kluc():
    with open(KEYS_DIR, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

# Načítanie verejného kľúča
def nacitaj_verejny_kluc():
    with open(KEYS_DIR2, "rb") as f:
        return serialization.load_pem_public_key(f.read())

# Digitálny podpis transakcie
def podpis_transakciu(transakcia):
    privatny_kluc = nacitaj_sukromny_kluc()
    podpis = privatny_kluc.sign(
        transakcia.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return podpis

# Overenie digitálneho podpisu
def over_podpis(transakcia, podpis):
    verejny_kluc = nacitaj_verejny_kluc()
    try:
        verejny_kluc.verify(
            podpis,
            transakcia.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True  # Podpis je platný

    except Exception as e:
        print(f" Overenie podpisu zlyhalo: {e}")
        return False
