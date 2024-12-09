#!/usr/bin/env python
from pipeline import PandasCsvProvider


def main() -> None:
    print(PandasCsvProvider("transactions-fair.csv").get())


if __name__ == "__main__":
    main()
