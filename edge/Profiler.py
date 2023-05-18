from threading import Thread

import psutil


class Profiler:
    def __init__(self):
        self.process = psutil.Process()
        self.cpu_usage = []
        self.memory_usage = []
        self.running = True

    def collect_resource_usage(self):
        while self.running:
            self.cpu_usage.append(self.process.cpu_percent(1))
            self.memory_usage.append(self.process.memory_info().rss / 1024 ** 2)

    def start(self):
        daemon = Thread(target=self.collect_resource_usage, daemon=True, name='Resource monitor')
        daemon.start()

    def stop(self):
        self.running = False

    def get_results(self):
        return self.cpu_usage, self.memory_usage
