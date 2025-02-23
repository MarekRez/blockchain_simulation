# 📦 Blockchain pre logistiku a prepravu

Tento projekt je simuláciou **blockchainu pre lodnú prepravu**, ktorý umožňuje sledovať zásielky, validovať transakcie a zabezpečiť transparentnosť údajov pomocou šifrovania a konsenzuálneho algoritmu.

---
## 🚀 **Funkcionalita**
✅ **Blockchain s dynamickou obtiažnosťou** – Bloky sa ťažia s nastaviteľnou obtiažnosťou (Proof-of-Work).  
✅ **Šifrovanie údajov** – Použitie **Fernet (AES-128)** na ochranu dát.  
✅ **Konsenzus uzlov** – Každý blok musí byť schválený viacerými uzlami.  
✅ **Prístupové práva** – Používateľské roly **manažér, vodič, colný úradník**.  
✅ **História zásielok a vlastníkov** – Možnosť sledovania zmien v čase.  
✅ **Predikcia ETA (odhadovaný čas doručenia)** – Vypočítava sa podľa vzdialenosti a rýchlosti.  
✅ **Protokol o kontrole kvality** – Monitorovanie **teploty, vlhkosti a poznámok** pri zásielkach.  
✅ **Vizualizácia údajov** – Použitie **Tkinter dashboardu** a **REST API (voliteľné)**.

---
## 🏗 **Štruktúra projektu**

```
📂 blockchain_project
│── 📂 blockchain
│   │── __init__.py           # Označuje priečinok ako Python balík
│   │── blockchain.py         # Hlavná logika blockchainu
│   │── block.py              # Trieda Blok (reprezentácia bloku)
│   │── encryption.py         # Šifrovanie (Fernet)
│   │── consensus.py          # Konsenzus algoritmus (hlasovanie uzlov)
│   │── permissions.py        # Prístupové práva a role
│   │── quality_check.py      # Kontrola kvality zásielok
│
│── 📂 ui
│   │── dashboard.py          # Tkinter dashboard pre vizualizáciu blockchainu
│
│── main.py                   # Hlavný skript na spustenie blockchainu
│── requirements.txt          # Zoznam knižníc (`pip install -r requirements.txt`)
│── README.md                 # Dokumentácia projektu
```

---
## ⚡ **Ako spustiť projekt**
### 1️⃣ **Nainštaluj závislosti**
```bash
pip install -r requirements.txt
```
### 2️⃣ **Spusti blockchain**
```bash
python main.py
```
### 3️⃣ **Zobrazenie šifrovaných údajov v blockchainu**
```bash
python -c "from blockchain.blockchain import Blockchain; b = Blockchain(); b.zobraz_sifrovane_udaje()"
```
### 4️⃣ **Spustenie dashboardu**
```bash
python -c "from ui.dashboard import zobraz_dashboard; zobraz_dashboard()"
```

---
## 📜 **Záver**
Tento projekt demonštruje **praktické využitie blockchainu v logistike**. Môže byť použitý na **sledovanie zásielok v reálnom čase**, **overenie transakcií** a **zvýšenie transparentnosti v dodávateľskom reťazci**. 🚀