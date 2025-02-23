ROLE_MANAGER = "manažér"
ROLE_DRIVER = "vodič"
ROLE_CUSTOMS = "colný úradník"

class Pouzivatel:
    def __init__(self, meno, rola):
        self.meno = meno
        self.rola = rola

PRISTUPOVE_PRAVIDLA = {
    "pridaj_zasielku": [ROLE_MANAGER],
    "aktualizuj_miesto": [ROLE_DRIVER],
    "prenesenie_majetku": [ROLE_MANAGER],
    "nahlad_na_udaje": [ROLE_MANAGER, ROLE_DRIVER, ROLE_CUSTOMS]
}
