import random
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s || %(message)s",
                    datefmt="%H:%M:%S")

fixed = 42

random_nums = [random.randint(-100, 100) for _ in range(10)]

for num in random_nums:
    try:
        if fixed % num == 0:
            logging.info(
                "42 делится на %s без остатка с результатом: %s", num,
                fixed // num)
        else:
            logging.warning("42 делится на %s с остатком с результатом: %s",
                            num, round(fixed / num, 3))
    except ZeroDivisionError:
        logging.error("Среди делителей встретился ноль")
