import pandas as pd


class Cleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(
            labels=["date", "transaction_id", "client_id", "product_id"], axis=1
        )
        for i in range(len(df)):
            if df["amount"][i] is None:
                continue
            if not df["amount"][i].isnumeric():
                df["amount"][i] = None
                continue
            if int(df["amount"][i]) < 1:
                df["amount"][i] = None
        return df.dropna(axis=0)


class PandasCsvProvider:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def get(self) -> pd.DataFrame:
        return pd.read_csv(self.path)
