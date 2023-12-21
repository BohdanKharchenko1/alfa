import multiprocessing
import random


class Generator:
    def __init__(self):
        self.predmety = {
            "Hrabalova:  M": 4,
            "Vobecky: DS Praxe": 2,
            "Vobecky: DS Teorie": 1,
            "Masopust: PSS Teorie": 1,
            "Masopust/Molic: PSS Praxe": 2,
            "Benda/Brcakova: PIS Praxe": 2,
            "Brcakova: PIS Teorie": 2,
            "Studenkova: CJ": 3,
            "Mandik/Reichlova: PV": 2,
            "Reichlova: PV": 1,
            "Hemzalova/Adamek: WA": 2,
            "Adamek: WA": 1,
            "Vana: CIT": 2,
            "Kallmunzer: AM": 2,
            "Mandik: TP": 1,
            "Paltikova/Juchelka AJ": 4,
            "Volno": 3
        }
        self.patra = {
            "1. patro": list(range(1, 6)),
            "2. patro": list(range(6, 11)),
            "3. patro": list(range(11, 16)),
            "4. patro": list(range(16, 21)),
        }
        self.MIN_HODIN_DEN = 4
        self.MAX_HODIN_DEN = 10
        self.DNY_V_TYDNU = 5
        self.pocet_vygenerovanych_rozvrhu = 0
        self.lock = multiprocessing.Lock()

        # Precompute available classrooms and subjects
        self.vsechny_ucebny = list({ucebna for patro in self.patra.values() for ucebna in patro})
        self.vsechny_predmety = list(self.predmety.keys())

        # Precompute all combinations of subjects and classrooms
        self.vsechny_kombinace = [(predmet, ucebna) for predmet in self.vsechny_predmety for ucebna in self.vsechny_ucebny]

    def generuj_rozvrh(self):
        rozvrh = {}

        for den in range(1, self.DNY_V_TYDNU + 1):
            pocet_hodin_v_den = random.randint(self.MIN_HODIN_DEN, self.MAX_HODIN_DEN)

            # Randomly select combinations from precomputed list
            vybrane_kombinace = random.sample(self.vsechny_kombinace, k=min(pocet_hodin_v_den, len(self.vsechny_kombinace)))

            # Ensure "Volno" is not the last subject
            if "Volno" in vybrane_kombinace:
                vybrane_kombinace.remove("Volno")
                vybrane_kombinace.append("Volno")

            # Split the selected combinations into subjects and classrooms
            predmety_v_dnu, ucebny_v_dnu = zip(*vybrane_kombinace)

            # Store the schedule in the desired format
            rozvrh[den] = {"predmety": predmety_v_dnu, "ucebny": ucebny_v_dnu}

        return rozvrh
