import Generator


class Hodnotitel:
    def __init__(self):
        # Předdefinované hodnoty bonusů/penále pro jednotlivá pravidla
        self.bonus_malus_pravidlo_1 = {
            "Pátek 9. hodina": -100,
            # další hodiny a jejich hodnocení...
        }

        self.bonus_malus_pravidlo_7 = {
            "Matematika": -50,
            "Profilové předměty": -30,
            # další předměty a jejich hodnocení...
        }

        self.bonus_malus_pravidlo_10 = {
            "Učitel A": -30,
            "Učitel B": -30,
            "Učitel C": -30,
            "Učitel X": 20,
            # další učitelé a jejich hodnocení...
        }

    def hodnot_pravidlo_1(self, hodina):
        # Pravidlo 1: Bonus/malus za každou hodinu v rozvrhu
        return self.bonus_malus_pravidlo_1.get(hodina, 0)

    def hodnot_pravidlo_2(self, rozvrh):
        # Pravidlo 2: Stejný předmět vícekrát v jeden den není dobré
        body = 0
        for den, hodiny in rozvrh.items():
            predmety_v_dnu = [hodina.split(":")[1].strip() for hodina in hodiny["predmety"]]
            pocet_vyskytu = {predmet: predmety_v_dnu.count(predmet) for predmet in set(predmety_v_dnu)}

            for predmet, pocet in pocet_vyskytu.items():
                if pocet > 1 and not predmet.endswith("hod"):
                    body -= 50  # Penalizujeme opakování předmětu v jednom dni
        return body

    def hodnot_pravidlo_3(self, rozvrh):
        # Pravidlo 3: Přecházení mezi patry a učebnami
        body = 0
        for den, hodiny in rozvrh.items():
            ucebny_v_dnu = hodiny["ucebny"]
            patra_v_dnu = {ucebna: self.najdi_patro(ucebna) for ucebna in ucebny_v_dnu}
            unikatni_patra = set(patra_v_dnu.values())

            if len(unikatni_patra) > 1:
                body -= 30  # Penalizujeme přecházení mezi patry
            elif len(set(ucebny_v_dnu)) > 1:
                body -= 20  # Penalizujeme přecházení mezi učebnami na stejném patře
        return body

    def hodnot_pravidlo_4(self, rozvrh):
        # Pravidlo 4: Obědy
        body = 0
        for den, hodiny in rozvrh.items():
            if hodiny["predmety"][0] in ["5. hodina", "6. hodina", "7. hodina", "8. hodina"]:
                body -= 40  # Penalizujeme, pokud je hodina 5.-8. určena na oběd
        return body

    def hodnot_pravidlo_5(self, rozvrh):
        # Pravidlo 5: Denní doba učení
        body = 0
        pocet_hodin_v_den = sum(len(hodiny["predmety"]) for hodiny in rozvrh.values())
        if pocet_hodin_v_den < 5 or pocet_hodin_v_den > 8:
            body -= 50  # Penalizujeme, pokud se učí méně než 5 hodin nebo více než 8 hodin denně
        return body

    def hodnot_pravidlo_6(self, rozvrh):
        # Pravidlo 6: Dvouhodinová a tříhodinová cvičení
        body = 0
        for den, hodiny in rozvrh.items():
            for i in range(len(hodiny["predmety"])):
                predmet = hodiny["predmety"][i]
                if predmet.endswith("Cvičení") and i < len(hodiny["predmety"]) - 1:
                    nasledujici_predmet = hodiny["predmety"][i + 1]
                    if nasledujici_predmet.endswith("Cvičení") and nasledujici_predmet != predmet:
                        body += 20  # Bonus za dvouhodinové a tříhodinové cvičení v jednom dni
        return body

    def hodnot_pravidlo_7(self, rozvrh):
        # Pravidlo 7: Matematika a profilové předměty
        body = 0
        for den, hodiny in rozvrh.items():
            for predmet in hodiny["predmety"]:
                if predmet in self.bonus_malus_pravidlo_7:
                    body += self.bonus_malus_pravidlo_7[predmet]
        return body

    def hodnot_pravidlo_8(self, rozvrh):
        # Pravidlo 8: Rozvrh bez volna
        body = 0
        for hodiny in rozvrh.values():
            if "Volno" not in hodiny["predmety"]:
                body -= 30  # Penalizujeme rozvrh bez volna
        return body

    def hodnot_pravidlo_9(self, rozvrh):
        # Pravidlo 9: Více než 6 profilových předmětů za den
        body = 0
        for den, hodiny in rozvrh.items():
            pocet_profilovych_predmetu = sum(
                1 for predmet in hodiny["predmety"] if predmet in self.bonus_malus_pravidlo_7)
            if pocet_profilovych_predmetu > 6:
                body -= 40  # Penalizujeme více než 6 profilových předmětů za den
        return body

    def hodnot_pravidlo_10(self, rozvrh):
        # Pravidlo 10: Wellbeing pravidlo
        body = 0
        for den, hodiny in rozvrh.items():
            for predmet in hodiny["predmety"]:
                if predmet in self.bonus_malus_pravidlo_10:
                    body += self.bonus_malus_pravidlo_10[predmet]
        return body

    def najdi_patro(self, ucebna):
        for patro, cisla_ucebny in Generator.patra.items():
            if ucebna in cisla_ucebny:
                return patro
        return None

    def hodnotit_rozvrh(self, rozvrh):
        body = 0

        body += self.hodnot_pravidlo_1("Pátek 9. hodina")
        body += self.hodnot_pravidlo_2(rozvrh)
        body += self.hodnot_pravidlo_3(rozvrh)
        body += self.hodnot_pravidlo_4(rozvrh)
        body += self.hodnot_pravidlo_5(rozvrh)
        body += self.hodnot_pravidlo_6(rozvrh)
        body += self.hodnot_pravidlo_7(rozvrh)
        body += self.hodnot_pravidlo_8(rozvrh)
        body += self.hodnot_pravidlo_9(rozvrh)
        body += self.hodnot_pravidlo_10(rozvrh)

        return body


