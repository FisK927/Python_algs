from functools import reduce


def new_round(el):
    return round(el, 2)


students = {"Greg": [3, 2, 5, 5], "Alex": [5, 2, 2, 2, 3, 5],
            "John": [4, 5, 4], "Peter": [2, 3, 3]}

if __name__ == "__main__":
    students_new = dict(
        map(lambda item: (item[0], new_round(sum(item[1]) / len(item[1]))),
            students.items()))
    total_grades = reduce(lambda acc, grades: acc + len(grades), students.values(), 0)

    print("Новый словарь со средними оценками:", students_new)
    print(f"Всего оценок: {total_grades}")
