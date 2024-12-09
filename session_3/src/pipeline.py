import pandas as pd


class Cleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(
            labels=["date", "transaction_id", "client_id", "product_id"], axis=1
        )
        valid_values = ["legit", "fraud", "high_risk", "low_risk"]
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df[df["amount"].notna() & (df["amount"] >= 1)]
        df = df[df["label"].isin(valid_values)]
        return df.dropna(axis=0)


class PandasCsvProvider:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def get(self) -> pd.DataFrame:
        return pd.read_csv(self.path)
