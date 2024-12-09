import pandas as pd


class Cleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        return df


class PandasCsvProvider:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def get(self) -> pd.DataFrame:
        return pd.read_csv(self.path)
