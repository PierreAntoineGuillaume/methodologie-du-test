#!/usr/bin/env python
from pipeline import PandasCsvProvider, Cleaner, Trainer


def main() -> None:
    provider = PandasCsvProvider("transactions-fair.csv")
    cleaner = Cleaner()
    trainer = Trainer()
    df = provider.get()
    df = cleaner.clean(df)
    model = trainer.train(df)
    print(model.metadata)



if __name__ == "__main__":
    main()
