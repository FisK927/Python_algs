import re


def validate(s):
    if not re.fullmatch(r"[a-zA-Z]+", s):
        exit("Строка должна состоять только из латинских букв (без пробелов)")
    return s


def encode(s):
    return re.sub(
        r"([a-zA-Z])\1*",
        lambda m: f"{m.group(1)}{len(m.group(0))}",
        s
    )


def decode(s):
    pairs = re.findall(r"([a-zA-Z])(\d+)", s)
    return "".join(char * int(count) for char, count in pairs)


if __name__ == "__main__":
    original = validate(input("Введите строку из латинских букв: "))

    encoded = encode(original)
    decoded = decode(encoded)

    print(f"Исходная:      {original}")
    print(f"Закодировано:  {encoded}")
    print(f"Раскодировано: {decoded}")

    if original == decoded:
        print("Строки совпадают")
    else:
        print("Строки не совпадают, странно...")
