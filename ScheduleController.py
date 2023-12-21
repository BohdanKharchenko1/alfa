class ScheduleController:
    def __init__(self, predmety, vsechny_predmety):
        self.predmety = predmety
        self.vsechny_predmety = vsechny_predmety

    def kontrola_rozvrhu(self, rozvrh):
        pocet_predmetu = {predmet: 0 for predmet in self.vsechny_predmety}

        for den in rozvrh.values():
            for predmet in den["predmety"]:
                pocet_predmetu[predmet] += 1

        for predmet, hodiny in self.predmety.items():
            if pocet_predmetu[predmet] != hodiny:
                return False
        return True
