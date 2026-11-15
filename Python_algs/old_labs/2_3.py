import re

pattern = r"(\S(?:.*\S)?) --- (\d+)(,\d{2})? (руб|коп)\."

try:
    n = int(input("Введите число товаров: ").strip())
except ValueError:
    exit("Нужно ввести целое число")

item_list = []
incorrect = 0
correct = []
list_a = []
seen = set()

for i in range(n):
    item_list.append(input("Введите название и цену: "))

for i in range(n):
    m = re.fullmatch(pattern, item_list[i])
    if m == None:
        incorrect += 1
    else:
        name = m.group(1)
        if name in seen:
            continue
        seen.add(name)
        rub = int(m.group(2))
        kop = int(m.group(3)[1:]) if m.group(3) != None else 0
        correct.append((name, rub, kop))
        if rub >= 1000:
            list_a.append([name, rub, kop])

list_a = sorted(list_a, key=lambda x: (-x[1], -x[2], x[0]))

summa = sum(map(lambda x: x[1] * 100 + x[2], correct))

for i in list_a:
    print(f"{i[0]}: {i[1]}.{i[2]:02d}")

print(f"\nИтого: {summa // 100}.{summa % 100:02d}")
print(f"Некорректных строк: {incorrect}")
