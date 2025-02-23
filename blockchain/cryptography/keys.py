from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def vygeneruj_kluce():
    # Vytvorenie súkromného a verejného kľúča
    privatny_kluc = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    verejny_kluc = privatny_kluc.public_key()

    # Uloženie kľúčov do súborov
    with open("private_key.pem", "wb") as f:
        f.write(privatny_kluc.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("public_key.pem", "wb") as f:
        f.write(verejny_kluc.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("Súkromný a verejný kľúč vygenerované.")

# Spustíme len raz na vygenerovanie kľúčov
vygeneruj_kluce()