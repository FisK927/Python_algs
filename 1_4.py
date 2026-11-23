import os
import re
from collections import defaultdict
import datetime


def parse_time(s):
    return datetime.datetime.strptime(s.strip(), "%d/%b/%Y:%H:%M:%S %z")


def status(pattern, file_path, start=None, end=None):
    if start and end and start > end:
        start, end = end, start

    cnt_errors = 0
    avg_size = defaultdict(list)

    with open(file_path, "r", encoding="UTF-8") as f:
        for string in f:
            fm = re.fullmatch(pattern, string)
            if not fm:
                print(f"Не учитывается: {string!r}")
                continue

            if start is not None and end is not None:
                t = parse_time(fm.group(4))
                if not (start <= t <= end):
                    continue

            status_code = fm.group(6)
            if status_code[0] in '45':
                cnt_errors += 1

            if fm.group(7) != '-':
                avg_size[status_code].append(int(fm.group(7)))

    for x in avg_size:
        avg_size[x] = round(sum(avg_size[x]) / len(avg_size[x]), 4)
    return cnt_errors, avg_size


clf_pattern = r'(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-)\r?\n?'

path = input("Введите путь к файлу access.log: ").strip()

if not path.endswith("access.log"):
    exit("Нужен путь к файлу access.log")
if not os.path.isfile(path):
    exit("Файл не найден")

try:
    start_time = parse_time(input(
        "Введите время начала в таком же формате 12/Oct/2025:10:39:03 +0300: "))
    end_time = parse_time(input(
        "Введите время конца в таком же формате 12/Oct/2025:10:39:03 +0300: "))
except ValueError:
    exit("Время должно быть в формате 12/Oct/2025:10:39:03 +0300")

try:
    cnt_errs, average = status(clf_pattern, path)
    cnt_errs_time, average_time = status(clf_pattern, path, start_time, end_time)
except PermissionError:
    exit("Доступ к файлу запрещён")
except UnicodeDecodeError:
    exit("Кодировка файла не UTF-8")

with open("result.txt", "w", encoding="UTF-8") as result:
    result.writelines([
        f"Средний размер ответа по коду состояния *код: размер* - {dict(average)}\n",
        f"Ошибок: {cnt_errs}\n",
        f"Средний размер ответа по коду состояния *код: размер* - {dict(average_time)}\n",
        f"Ошибок: {cnt_errs_time}\n"])
