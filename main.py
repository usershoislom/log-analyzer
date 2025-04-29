import argparse
import sys
from reports.base import REPORT_TYPES
import reports.handlers


def parse_args():
    parser = argparse.ArgumentParser(description="Генерация отчётов на основе логов.")
    parser.add_argument("files", nargs="+", help="Файлы логов для обработки")
    parser.add_argument("--report", required=True, choices=REPORT_TYPES.keys(), help="Название отчёта")
    return parser.parse_args()


def main():
    args = parse_args()

    report_class = REPORT_TYPES.get(args.report)
    if not report_class:
        print(f"Ошибка: отчёт '{args.report}' не найден.")
        print(f"Доступные отчёты: {', '.join(REPORT_TYPES.keys())}")
        sys.exit(1)

    report = report_class(args.files)
    report.run()


if __name__ == "__main__":
    main()
