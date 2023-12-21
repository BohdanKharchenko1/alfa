class ScheduleOutput:
    def __init__(self, lock):
        self.lock = lock

    def vypis_rozvrh(self, rozvrh):
        with self.lock:
            print("Generovaný rozvrh:")
            for den, data in rozvrh.items():
                print(f"Den {den}:")
                for ucebna, predmet in zip(data["ucebny"], data["predmety"]):
                    if predmet == "Volno":
                        print(f"   {predmet}")
                    else:
                        print(f"   {ucebna} {predmet}")
            print("\n")