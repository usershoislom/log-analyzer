import argparse
import sys
from reports import REPORT_TYPES


def parse_args():
    parser = argparse.ArgumentParser(description="Генерация отчётов")
    parser.add_argument("files", nargs="+", help="Файлы логов для обработки")
    parser.add_argument(
        "--report",
        required=True,
        choices=REPORT_TYPES.keys(),
        help="введите название отчёта",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    report_class = REPORT_TYPES.get(args.report)
    report = report_class(args.files)
    report.run()


if __name__ == "__main__":
    main()
