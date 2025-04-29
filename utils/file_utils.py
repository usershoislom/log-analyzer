import os


def process_file(file_paths: list[str]):
    # content = ""

    for file_path in file_paths:
        if not os.path.isfile(file_path):
            print(f"ошибка с доступом к файлу: {file_path}")
        else:
            with open(file_path, "r") as f:
                content = f.readlines()
                print(f"Файл {file_path} содержит {len(content)} запросов")

