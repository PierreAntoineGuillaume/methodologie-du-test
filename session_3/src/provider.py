import csv
from typing import Any


class Provider:
    def __init__(self) -> None:
        pass
    def get(self) -> list[Any]:
        with open("transactions-fair.csv", "r") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        return data
