from abc import ABC, abstractmethod
import os
import re
import sys
from collections import defaultdict as dt

from typing_extensions import Any

REPORT_TYPES: dict[str, type] = {}
LOG_LEVELS: list[str] = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseReport(ABC):
    def __init__(self, files: list[str]) -> None:
        self.files = files
        self.total_requests = 0
        self.report_content = ""
        self.counter: dt[Any, dt[Any, int]] = dt(lambda: dt(int))
        self.summary = {lvl: 0 for lvl in LOG_LEVELS}
        self._validate_files()

    def _validate_files(self) -> None:
        for path in self.files:
            if not os.path.isfile(path):
                print(f"Ошибка: файл {path} не найден или не является файлом.")
                sys.exit(1)

    @staticmethod
    def extract_log_level(line: str) -> str | None:
        for level in LOG_LEVELS:
            if level in line:
                return level
        return None

    @staticmethod
    def extract_endpoint(line: str) -> str | None:
        if "django.request" in line:
            match = re.search(r"/(api|admin)[^\s]*", line)
            if match:
                return match.group(0)
        return None

    def print_summary(self) -> None:
        print(f"\nTotal requests: {self.total_requests}\n")
        handler_column = f"{'HANDLER':<30}"
        log_levels_columns = "\t".join([f"{lvl:<7}" for lvl in LOG_LEVELS])
        header = handler_column + log_levels_columns
        print(header)

        for path in sorted(self.counter):
            row = f"{path:<30}"
            for lvl in LOG_LEVELS:
                count = self.counter[path][lvl]
                row += f"{count:<7}\t"
                self.summary[lvl] += count
            print(row)

        summary_row = f"{'TOTAL':<30}" + "\t".join(
            [f"{self.summary[lvl]:<7}" for lvl in LOG_LEVELS]
        )
        print(summary_row)

    def run(self) -> None:
        self.process()
        self.generate()

    @abstractmethod
    def process(self) -> None:
        pass

    @abstractmethod
    def generate(self) -> None:
        pass


def register_report(name: str):
    def decorator(cls):
        REPORT_TYPES[name] = cls
        return cls

    return decorator
