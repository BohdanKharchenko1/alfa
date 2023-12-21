import sys
import time


class Watchdog:
    def __init__(self, timeout=10, lock=None):
        self.timeout = timeout
        self.start_time = time.time()
        self.lock = lock

    def check_timeout(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.timeout

    def run(self):
        while not self.check_timeout():
            time.sleep(1)

        with self.lock:
            print("Timeout reached. Terminating processes.")
        sys.exit(0)