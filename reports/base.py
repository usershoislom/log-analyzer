from abc import ABC, abstractmethod


REPORT_TYPES = {}


class BaseReport(ABC):
    def __init__(self, files):
        self.files = files
        self.report_content = ""
        self.total_requests = 0

    @abstractmethod
    def process(self):
        """Обработать файлы"""
        pass

    @abstractmethod
    def generate(self):
        """Сформировать содержимое отчёта"""
        pass

    def run(self):
        self.process()
        self.generate()


def register_report(name):
    def decorator(cls):
        REPORT_TYPES[name] = cls
        return cls
    return decorator

