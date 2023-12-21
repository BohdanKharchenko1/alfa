import multiprocessing
import os

from Generator import Generator
from ScheduleController import ScheduleController
from ScheduleOutput import ScheduleOutput
from Watchdog import Watchdog


def main():
    rozvrh_generator = Generator()
    rozvrh_kontrolor = ScheduleController(rozvrh_generator.predmety, rozvrh_generator.vsechny_predmety)
    vypisovac = ScheduleOutput(rozvrh_generator.lock)
    watchdog = Watchdog(lock=rozvrh_generator.lock)

    pocet_procesu = os.cpu_count()
    with multiprocessing.Pool(processes=pocet_procesu) as pool:
        watchdog_process = multiprocessing.Process(target=watchdog.run)
        watchdog_process.start()

        results = []

        while not watchdog.check_timeout():
            rozvrh = rozvrh_generator.generuj_rozvrh()

            if rozvrh_kontrolor.kontrola_rozvrhu(rozvrh):
                result = pool.apply_async(vypisovac.vypis_rozvrh, args=(rozvrh,))
                results.append(result)

            rozvrh_generator.pocet_vygenerovanych_rozvrhu += 1

        watchdog_process.join()

        for result in results:
            result.get()

        pool.close()
        pool.join()
        print(f"Celkový počet vygenerovaných rozvrhů: {rozvrh_generator.pocet_vygenerovanych_rozvrhu}")


if __name__ == "__main__":
    main()
