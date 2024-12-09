import pandas as pd

from pipeline import Cleaner


def test_clean_dataframe() -> None:
    df = pd.DataFrame(
        {
            "transaction_id": [None],
            "client_id": ["1"],
            "product_id": ["1"],
            "amount": ["25"],
            "date": ["2024-01-01"],
            "label": ["legit"],
        }
    )
    cleaner = Cleaner()
    df = cleaner.clean(df)
    print(df)
    assert df.empty
