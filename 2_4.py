import os
import shutil


cur_dir = input("Введите путь к архиву: ")
archive_path = cur_dir

if not os.path.isfile(archive_path):
    exit("Архив не найден")

temp_dir = os.path.join(os.getcwd(), "temp")
os.makedirs(temp_dir, exist_ok=True)
try:
    shutil.unpack_archive(archive_path, temp_dir)
except shutil.ReadError:
    exit("Ошибка чтения архива")
except PermissionError:
    exit("Нет доступа")
total_size = 0

for cur_dir, dirs, files in os.walk(temp_dir):
    for file in files:
        full_file_path = os.path.join(cur_dir, file)
        total_size += os.path.getsize(full_file_path)

shutil.rmtree(temp_dir)

print(f"Суммарный размер файлов: {total_size} байт")
