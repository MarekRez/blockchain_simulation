import tkinter as tk
from tkinter import ttk
from blockchain.blockchain import Blockchain

# Inicializácia blockchainu
blockchain = Blockchain()

def aktualizuj_dashboard(tree):
    """Obnoví údaje v tabuľke"""
    for row in tree.get_children():
        tree.delete(row)

    df = blockchain.ziskaj_data()
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.after(5000, lambda: aktualizuj_dashboard(tree))  # Automatická aktualizácia každých 5 sekúnd

def zobraz_dashboard():
    """Vytvorí a zobrazí GUI dashboardu"""
    root = tk.Tk()
    root.title("Blockchain Dashboard")

    # Vytvorenie tabuľky
    tree = ttk.Treeview(root)
    df = blockchain.ziskaj_data()

    tree["columns"] = list(df.columns)
    tree.column("#0", width=0, stretch=tk.NO)

    for col in df.columns:
        tree.column(col, anchor=tk.W, width=150)
        tree.heading(col, text=col, anchor=tk.W)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill="both")

    # Automatická aktualizácia
    tree.after(5000, lambda: aktualizuj_dashboard(tree))

    root.mainloop()

# Ak sa súbor spustí samostatne, otvorí dashboard
if __name__ == "__main__":
    zobraz_dashboard()
