import os
import sys

from reports.base import BaseReport, register_report


@register_report("handlers")
class HandlersReport(BaseReport):
    def __init__(self, files):
        super().__init__(files)

    def process(self):
        for path in self.files:
            if not os.path.isfile(path):
                print(f"Ошибка: файл {path} не найден.")
                sys.exit(1)
            with open(path, 'r') as f:
                for line in f:
                    if "django.request" in line:
                        self.report_content += line
                        self.total_requests += 1

    def generate(self):
        print(self.report_content)
        print(self.total_requests)