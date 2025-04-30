from abc import ABC, abstractmethod
import os
import re
import sys
from collections import defaultdict

REPORT_TYPES = {}
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseReport(ABC):
    def __init__(self, files):
        self.files = files
        self.total_requests = 0
        self.report_content = ""
        self.counter = defaultdict(lambda: defaultdict(int))
        self.summary = {lvl: 0 for lvl in LOG_LEVELS}
        self._validate_files()

    def _validate_files(self):
        for path in self.files:
            if not os.path.isfile(path):
                print(f"Ошибка: файл {path} не найден или не является файлом.")
                sys.exit(1)

    def extract_log_level(self, line):
        for level in LOG_LEVELS:
            if level in line:
                return level
        return None

    def extract_endpoint(self, line):
        if "django.request" not in line:
            return None
        match = re.search(r'/(api|admin)[^\s]*', line)
        if match:
            return match.group(0)
        return None

    def print_summary(self):
        print(f"\nTotal requests: {self.total_requests}\n")
        header = f"{'HANDLER':<30}" + "\t".join([f"{lvl:<7}" for lvl in LOG_LEVELS])
        print(header)

        for path in sorted(self.counter):
            row = f"{path:<30}"
            for lvl in LOG_LEVELS:
                count = self.counter[path][lvl]
                row += f"{count:<7}\t"
                self.summary[lvl] += count
            print(row)

        summary_row = f"{'TOTAL':<30}" + "\t".join([f"{self.summary[lvl]:<7}" for lvl in LOG_LEVELS])
        print(summary_row)

    def run(self):
        self.process()
        self.generate()

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def generate(self):
        pass


def register_report(name):
    def decorator(cls):
        REPORT_TYPES[name] = cls
        return cls
    return decorator
